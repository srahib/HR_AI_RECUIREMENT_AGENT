from sqlalchemy import Column, Integer, String, Float, Text

from database import Base

# ==========================
# ADMIN TABLE
# ==========================
class Admin(Base):

    __tablename__ = "admins"

    id = Column(Integer, primary_key=True, index=True)

    username = Column(String, unique=True)

    password = Column(String)

# ==========================
# CANDIDATE TABLE
# ==========================
class Candidate(Base):

    __tablename__ = "candidates"

    id = Column(Integer, primary_key=True, index=True)

    file_name = Column(String)

    name = Column(String)

    email = Column(String, unique=True)

    phone = Column(String)

    age = Column(Integer)

    education = Column(String)

    experience = Column(Integer)

    skills = Column(Text)

    ai_score = Column(Float)

    final_score = Column(Float)

    recommendation = Column(String)

    resume_text = Column(Text)
