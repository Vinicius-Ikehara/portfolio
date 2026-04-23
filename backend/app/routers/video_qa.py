"""Video Agent router — file upload + chat with Gemini."""
import logging
import re
import secrets
import filetype
from fastapi import APIRouter, Depends, Header, HTTPException, BackgroundTasks, Request, UploadFile, File, status
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from ..database import get_db, SessionLocal
from ..rate_limit import limiter
from ..models import VideoQASession, VideoQAStatus
from ..config import settings
from ..services.gemini_video import (
    upload_video_file,
    transcribe_video,
    chat_with_video,
    delete_gemini_file,
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/video-qa", tags=["video-agent"])

ALLOWED_VIDEO_MIME_PREFIX = "video/"
ALLOWED_VIDEO_EXTENSIONS = {"mp4", "mov", "webm", "mkv", "avi", "m4v", "3gp", "flv", "wmv"}
MAX_UPLOAD_BYTES = 100 * 1024 * 1024  # 100MB
_FILENAME_SAFE_RE = re.compile(r"[^\w.\-]+")


def _sanitize_filename(raw: str | None) -> str:
    if not raw:
        return "video"
    base = raw.replace("\\", "/").rsplit("/", 1)[-1]
    cleaned = _FILENAME_SAFE_RE.sub("_", base).strip("._") or "video"
    return cleaned[:120]


def _load_session_or_403(session_id: int, token: str | None, db: Session) -> VideoQASession:
    # Constant-time comparison on a token that must exist — stops ID enumeration
    # from distinguishing "session exists" vs "wrong token".
    row = db.query(VideoQASession).filter(VideoQASession.id == session_id).first()
    if not row or not row.session_token or not token or not secrets.compare_digest(row.session_token, token):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid session or missing token.")
    return row


class CreateSessionResponse(BaseModel):
    id: int
    session_token: str
    status: str


class SessionStatusResponse(BaseModel):
    id: int
    original_filename: str | None
    video_title: str | None
    duration_seconds: int | None
    status: str
    has_transcript: bool
    error_message: str | None


class ChatMessage(BaseModel):
    role: str
    content: str = Field(..., max_length=10000)


class ChatRequest(BaseModel):
    pergunta: str = Field(..., min_length=1, max_length=2000)
    history: list[ChatMessage] = Field(default_factory=list, max_length=50)


class ChatResponse(BaseModel):
    resposta: str


def _friendly_gemini_error(exc: Exception, fallback: str) -> str:
    raw = str(exc)
    if "API_KEY_INVALID" in raw or "API key not" in raw.lower():
        return "Gemini API key is invalid or revoked. Generate a new one at https://aistudio.google.com/apikey and update your environment."
    if "RESOURCE_EXHAUSTED" in raw or "429" in raw:
        return "Gemini quota exceeded. Please try again in a few minutes."
    if "UNAVAILABLE" in raw or "503" in raw or "high demand" in raw.lower():
        return "Gemini is currently under high demand. Please try again in a few minutes."
    if "INVALID_ARGUMENT" in raw or "400" in raw:
        return "Gemini rejected the video. Please try a different file."
    return fallback


def _run_full_pipeline(
    session_id: int,
    file_bytes: bytes,
    mime_type: str,
    display_name: str,
    api_key: str,
    max_seconds: int,
):
    """Background pipeline: upload → wait ACTIVE → validate duration → transcribe → cleanup.

    This runs after the HTTP response is sent, so the endpoint itself returns quickly
    and no reverse-proxy timeout is exceeded during Gemini's file-processing wait.
    """
    import asyncio
    db = SessionLocal()
    file_name_to_delete = None
    try:
        session_row = db.query(VideoQASession).filter(VideoQASession.id == session_id).first()
        if not session_row:
            return

        # Step 1 — upload to Gemini File API and wait for ACTIVE state
        try:
            uploaded = asyncio.run(
                upload_video_file(
                    file_bytes=file_bytes,
                    mime_type=mime_type,
                    api_key=api_key,
                    display_name=display_name,
                )
            )
        except Exception as exc:
            logger.exception("video_agent upload failed")
            session_row.status = VideoQAStatus.error
            session_row.error_message = _friendly_gemini_error(
                exc, "Failed to upload the video to Gemini. Please try again."
            )
            db.commit()
            return

        file_uri = uploaded["file_uri"]
        file_name_to_delete = uploaded.get("file_name")
        duration = uploaded.get("duration_seconds")

        # Persist Gemini references immediately so later cleanup always has a handle.
        session_row.gemini_file_uri = file_uri
        session_row.gemini_file_name = file_name_to_delete
        session_row.duration_seconds = duration
        db.commit()

        # Step 2 — reject videos that exceed our token budget
        if duration is not None and duration > max_seconds:
            mins, secs = divmod(duration, 60)
            limit_mins = max_seconds // 60
            session_row.status = VideoQAStatus.error
            session_row.error_message = (
                f"Video is {mins}min{secs:02d}s. Limit is {limit_mins} minutes to save tokens."
            )
            db.commit()
            return

        # Step 3 — transcribe with Gemini (multimodal audio+visual fusion)
        try:
            title, transcript = asyncio.run(transcribe_video(file_uri, mime_type, api_key))
            if title:
                session_row.video_title = title
            session_row.transcript_markdown = transcript
            session_row.status = VideoQAStatus.ready
            session_row.error_message = None
        except Exception as exc:
            logger.exception("video_agent transcription failed")
            session_row.status = VideoQAStatus.error
            session_row.error_message = _friendly_gemini_error(
                exc, "Failed to process the video. Please try a different file."
            )
        db.commit()
    finally:
        db.close()
        if file_name_to_delete:
            try:
                asyncio.run(delete_gemini_file(file_name_to_delete, api_key))
            except Exception:
                logger.warning("post-pipeline gemini cleanup failed for %s", file_name_to_delete)


@router.post("/sessions", response_model=CreateSessionResponse, status_code=status.HTTP_202_ACCEPTED)
@limiter.limit("3/minute;20/hour;50/day")
async def create_session(
    request: Request,
    background_tasks: BackgroundTasks,
    video: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    mime_type = (video.content_type or "").lower()
    if not mime_type.startswith(ALLOWED_VIDEO_MIME_PREFIX):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="File is not a video. Please upload mp4, mov, webm, etc.",
        )

    file_bytes = await video.read()
    size = len(file_bytes)
    if size == 0:
        raise HTTPException(status_code=422, detail="Empty file.")
    if size > MAX_UPLOAD_BYTES:
        mb = size / (1024 * 1024)
        limit_mb = MAX_UPLOAD_BYTES // (1024 * 1024)
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"File is {mb:.1f}MB. Limit is {limit_mb}MB.",
        )

    # Magic-bytes: Content-Type is client-supplied and forgeable, so the real file signature must match.
    kind = filetype.guess(file_bytes[:262])
    if kind is None or kind.extension not in ALLOWED_VIDEO_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="File signature does not match a valid video.",
        )
    mime_type = kind.mime  # use the detected MIME, not the client-provided one

    display_name = _sanitize_filename(video.filename)
    session_token = secrets.token_urlsafe(32)

    # Create the session row immediately so the client can start polling.
    # The full Gemini pipeline (upload → wait ACTIVE → validate duration → transcribe → cleanup)
    # runs in the background to keep this endpoint under any reverse-proxy timeout.
    new_session = VideoQASession(
        session_token=session_token,
        gemini_file_uri=None,
        original_filename=display_name,
        status=VideoQAStatus.processing,
    )
    db.add(new_session)
    db.commit()
    db.refresh(new_session)

    background_tasks.add_task(
        _run_full_pipeline,
        new_session.id,
        file_bytes,
        mime_type,
        display_name,
        settings.GEMINI_API_KEY,
        settings.VIDEO_QA_MAX_DURATION_SECONDS,
    )
    return CreateSessionResponse(id=new_session.id, session_token=session_token, status=new_session.status.value)


@router.get("/sessions/{session_id}", response_model=SessionStatusResponse)
def get_session(
    session_id: int,
    x_session_token: str | None = Header(default=None, alias="X-Session-Token"),
    db: Session = Depends(get_db),
):
    row = _load_session_or_403(session_id, x_session_token, db)
    return SessionStatusResponse(
        id=row.id,
        original_filename=row.original_filename,
        video_title=row.video_title,
        duration_seconds=row.duration_seconds,
        status=row.status.value if hasattr(row.status, "value") else str(row.status),
        has_transcript=bool(row.transcript_markdown),
        error_message=row.error_message,
    )


@router.post("/sessions/{session_id}/chat", response_model=ChatResponse)
@limiter.limit("20/minute;200/hour")
async def chat_session(
    request: Request,
    session_id: int,
    payload: ChatRequest,
    x_session_token: str | None = Header(default=None, alias="X-Session-Token"),
    db: Session = Depends(get_db),
):
    row = _load_session_or_403(session_id, x_session_token, db)
    status_value = row.status.value if hasattr(row.status, "value") else str(row.status)
    if status_value != "ready":
        raise HTTPException(status_code=409, detail=f"Session is not ready. Current status: {status_value}")
    if not row.transcript_markdown:
        raise HTTPException(status_code=409, detail="Transcript is not available.")
    try:
        history_dicts = [m.model_dump() for m in payload.history]
        resposta = await chat_with_video(
            transcript=row.transcript_markdown,
            history=history_dicts,
            question=payload.pergunta,
            api_key=settings.GEMINI_API_KEY,
        )
        return ChatResponse(resposta=resposta)
    except Exception:
        logger.exception("video_agent chat failed")
        raise HTTPException(status_code=500, detail="Error generating response.")
