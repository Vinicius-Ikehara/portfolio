from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import httpx
from app.config import settings

router = APIRouter(prefix="/api/webhook", tags=["webhook"])


class PokedexRequest(BaseModel):
    pergunta: str
    sessionId: str


@router.post("/pokedex")
async def proxy_pokedex(request: PokedexRequest):
    """
    Proxy endpoint for Pokedex webhook.
    Forwards requests to n8n and returns the response.
    """
    try:
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                settings.WEBHOOK_URL,
                json={
                    "pergunta": request.pergunta,
                    "sessionId": request.sessionId
                },
                headers={
                    "Content-Type": "application/json",
                    "Accept": "application/json"
                }
            )

            if response.status_code != 200:
                raise HTTPException(
                    status_code=response.status_code,
                    detail=f"n8n webhook error: {response.text}"
                )

            return response.json()

    except httpx.TimeoutException:
        raise HTTPException(status_code=504, detail="Webhook timeout")
    except httpx.RequestError as e:
        raise HTTPException(status_code=502, detail=f"Connection error: {str(e)}")
