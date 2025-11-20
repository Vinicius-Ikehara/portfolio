from pydantic import BaseModel
from typing import Optional, List, Dict
from datetime import datetime


# Project Schemas
class ProjectBase(BaseModel):
    title: str
    description: str
    technologies: List[str] = []
    image_url: Optional[str] = None
    project_url: Optional[str] = None
    github_url: Optional[str] = None
    order: int = 0


class ProjectCreate(ProjectBase):
    pass


class ProjectUpdate(ProjectBase):
    title: Optional[str] = None
    description: Optional[str] = None


class Project(ProjectBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


# Experience Schemas
class ExperienceBase(BaseModel):
    company: str
    position: str
    description: str
    technologies: List[str] = []
    start_date: str
    end_date: Optional[str] = None
    current: bool = False
    order: int = 0


class ExperienceCreate(ExperienceBase):
    pass


class ExperienceUpdate(ExperienceBase):
    company: Optional[str] = None
    position: Optional[str] = None
    description: Optional[str] = None


class Experience(ExperienceBase):
    id: int

    class Config:
        from_attributes = True


# Profile Schemas
class ProfileBase(BaseModel):
    name: str
    title: str
    bio: str
    email: Optional[str] = None
    phone: Optional[str] = None
    location: Optional[str] = None
    avatar_url: Optional[str] = None
    social_links: Dict[str, str] = {}
    skills: List[str] = []


class ProfileCreate(ProfileBase):
    pass


class ProfileUpdate(ProfileBase):
    name: Optional[str] = None
    title: Optional[str] = None
    bio: Optional[str] = None


class Profile(ProfileBase):
    id: int

    class Config:
        from_attributes = True
