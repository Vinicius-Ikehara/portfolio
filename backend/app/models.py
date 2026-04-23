import enum
from sqlalchemy import Column, Integer, String, Text, DateTime, JSON
from sqlalchemy import Enum as SAEnum
from datetime import datetime
from .database import Base


class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    technologies = Column(JSON)  # Lista de tecnologias usadas
    image_url = Column(String)
    project_url = Column(String)
    github_url = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    order = Column(Integer, default=0)  # Para ordenação customizada


class Experience(Base):
    __tablename__ = "experiences"

    id = Column(Integer, primary_key=True, index=True)
    company = Column(String, nullable=False)
    position = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    technologies = Column(JSON)  # Lista de tecnologias usadas
    start_date = Column(String, nullable=False)  # Ex: "2023-01"
    end_date = Column(String)  # None se ainda trabalha lá
    current = Column(Integer, default=0)  # 1 se é o emprego atual
    order = Column(Integer, default=0)


class Profile(Base):
    __tablename__ = "profile"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    title = Column(String, nullable=False)  # Ex: "Desenvolvedor IA"
    bio = Column(Text, nullable=False)
    email = Column(String)
    phone = Column(String)
    location = Column(String)
    avatar_url = Column(String)
    social_links = Column(JSON)  # {"github": "url", "linkedin": "url", ...}
    skills = Column(JSON)  # Lista de habilidades principais


class VideoQAStatus(str, enum.Enum):
    processing = "processing"
    ready = "ready"
    error = "error"


class VideoQASession(Base):
    __tablename__ = "video_qa_sessions"

    id = Column(Integer, primary_key=True, index=True)
    session_token = Column(String, nullable=True, index=True, unique=True)
    gemini_file_uri = Column(String, nullable=True)
    gemini_file_name = Column(String, nullable=True)
    original_filename = Column(String, nullable=True)
    duration_seconds = Column(Integer, nullable=True)
    video_title = Column(String, nullable=True)
    transcript_markdown = Column(Text, nullable=True)
    status = Column(SAEnum(VideoQAStatus), default=VideoQAStatus.processing, nullable=False)
    error_message = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
