from pydantic import BaseModel, EmailStr
from typing import Optional


# ==========================
# ADMIN
# ==========================

from pydantic import BaseModel

class AdminLogin(BaseModel):
    username: str
    password: str


# ==========================
# COMPANY
# ==========================

class CompanyCreate(BaseModel):
    organization_name: str
    job_title: str
    required_skills: str


class CompanyResponse(BaseModel):
    id: int
    organization_name: str
    job_title: str
    required_skills: str

    class Config:
        from_attributes = True


# ==========================
# CANDIDATE
# ==========================

class CandidateResponse(BaseModel):
    id: int
    file_name: Optional[str]
    name: Optional[str]
    email: Optional[EmailStr]
    phone: Optional[str]
    age: Optional[int]
    education: Optional[str]
    experience: Optional[int]
    skills: Optional[str]
    ai_score: Optional[float]
    final_score: Optional[float]
    recommendation: Optional[str]

    class Config:
        from_attributes = True