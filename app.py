from fastapi import FastAPI, UploadFile, File
from typing import List
from fastapi.responses import FileResponse
import glob
import os
from database import engine
from models import Base
Base.metadata.create_all(bind=engine)
from fastapi.responses import HTMLResponse
from fastapi import Request

from config import *

from parser import (
    extract_text_from_pdf,
    extract_text_from_docx,
    extract_candidate_info
)

from scoring import (
    calculate_score, get_recommendation
    )

from ranking import rank_candidates

from excel_export import export_excel


# -----------------------------
# APP
# -----------------------------
from fastapi.staticfiles import StaticFiles 
from fastapi.templating import Jinja2Templates
from auth import router as auth_router
app = FastAPI(
    title="HR AI Recruitment Agent",
    version="2.0"
)
app.include_router(auth_router)
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

UPLOAD_FOLDER = "resumes"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

REPORT_FOLDER = "reports"
os.makedirs(REPORT_FOLDER, exist_ok=True)

JOB_DESCRIPTION = f"""
{JOB_TITLE}

{" ".join(REQUIRED_SKILLS)}
"""

resumes_data = []


# -----------------------------
# HOME
# -----------------------------
@app.get("/", response_class=HTMLResponse)
def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

# -----------------------------
# UPLOAD RESUMES
# -----------------------------
@app.post("/upload-resumes")
async def upload_resumes(
    files: List[UploadFile] = File(...)
):

    global resumes_data

    resumes_data.clear()
    for file_path in glob.glob(os.path.join(UPLOAD_FOLDER, "*")):
        try:
            os.remove(file_path)
        except Exception:
            pass
    for file_path in glob.glob(os.path.join(REPORT_FOLDER, "*.xlsx")):
        try:
            os.remove(file_path)
        except Exception:
            pass

    uploaded = []

    for file in files:

        filepath = os.path.join(
            UPLOAD_FOLDER,
            file.filename
        )

        with open(filepath, "wb") as buffer:
            buffer.write(await file.read())

        extension = os.path.splitext(
            file.filename
        )[1].lower()

        if extension == ".pdf":
            resume_text = extract_text_from_pdf(filepath)

        elif extension == ".docx":
            resume_text = extract_text_from_docx(filepath)

        else:
            continue

        info = extract_candidate_info(resume_text)

        candidate = {
            "file_name": file.filename,
            "name": info["name"],
            "email": info["email"],
            "phone": info["phone"],
            "skills": info["skills"],
            "experience": info["experience"],
            "age": info["age"],
            "education": info["education"],
            "text": resume_text
        }

        duplicate = False

        for item in resumes_data:

            if (
                item["email"] == candidate["email"]
                and item["phone"] == candidate["phone"]
            ):
                duplicate = True
                break

        if duplicate:
            continue

        candidate["score"] = calculate_score(candidate)
        candidate["recommendation"] = get_recommendation(
            candidate["score"]
        )

        resumes_data.append(candidate)
        uploaded.append(file.filename)

    return {
        "message": "Upload Completed",
        "uploaded_files": uploaded,
        "total_uploaded": len(uploaded)
    }

# -----------------------------
# TOP 10 CANDIDATES
# -----------------------------
@app.get("/top-candidates")
def top_candidates():

    if len(resumes_data) == 0:
        return {
            "message": "No resumes uploaded"
        }

    top10 = rank_candidates(
        JOB_DESCRIPTION,
        resumes_data,
        TOP_CANDIDATES
    )

    return {
        "organization": ORGANIZATION_NAME,
        "job_title": JOB_TITLE,
        "total_resumes": len(resumes_data),
        "selected_candidates": len(top10),
        "top_candidates": top10
    }


# -----------------------------
# CANDIDATE DETAILS
# -----------------------------
@app.get("/candidate/{candidate_email}")
def candidate_details(candidate_email: str):

    for candidate in resumes_data:

        if candidate["email"].lower() == candidate_email.lower():

            return {
                "candidate": candidate
            }

    return {
        "message": "Candidate not found"
    }


# -----------------------------
# SEARCH BY SKILL
# -----------------------------
@app.get("/search-skill/{skill}")
def search_skill(skill: str):

    result = []

    for candidate in resumes_data:

        if skill.lower() in [
            s.lower() for s in candidate["skills"]
        ]:
            result.append(candidate)

    return {
        "skill": skill,
        "total": len(result),
        "candidates": result
    }


# -----------------------------
# SEARCH BY EXPERIENCE
# -----------------------------
@app.get("/search-experience/{years}")
def search_experience(years: int):

    result = []

    for candidate in resumes_data:

        if candidate["experience"] >= years:
            result.append(candidate)

    return {
        "minimum_experience": years,
        "total": len(result),
        "candidates": result
    }
# -----------------------------
# EXPORT EXCEL
# -----------------------------
@app.get("/export-excel")
def export_excel_api():

    if len(resumes_data) == 0:
        return {
            "message": "No resumes uploaded"
        }

    top10 = rank_candidates(
        JOB_DESCRIPTION,
        resumes_data,
        TOP_CANDIDATES
    )

    filename = export_excel(
        top10,
        ORGANIZATION_NAME,
        JOB_TITLE
    )

    return FileResponse(
        path=filename,
        filename=os.path.basename(filename),
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
# -----------------------------
# EXPORT SUMMARY
# -----------------------------
@app.get("/summary")
def summary():

    if len(resumes_data) == 0:
        return {
            "message": "No resumes uploaded"
        }

    top10 = rank_candidates(
        JOB_DESCRIPTION,
        resumes_data,
        TOP_CANDIDATES
    )

    highest_score = max(
        candidate["final_score"] for candidate in top10
    )

    average_score = round(
        sum(candidate["final_score"] for candidate in top10)
        / len(top10),
        2
    )

    return {
        "organization": ORGANIZATION_NAME,
        "job_title": JOB_TITLE,
        "total_uploaded": len(resumes_data),
        "top_candidates": len(top10),
        "highest_score": highest_score,
        "average_score": average_score
    }


# -----------------------------
# DELETE ALL RESUMES
# -----------------------------
@app.delete("/clear")
def clear_database():

    global resumes_data

    resumes_data.clear()

    return {
        "message": "All resumes cleared successfully"
    }
# -----------------------------
# DASHBOARD
# -----------------------------
@app.get("/dashboard")
def dashboard():

    total = len(resumes_data)

    selected = len(
        [c for c in resumes_data
         if c["recommendation"] == "Selected"]
    )

    interview = len(
        [c for c in resumes_data
         if c["recommendation"] == "Interview"]
    )

    rejected = len(
        [c for c in resumes_data
         if c["recommendation"] == "Rejected"]
    )

    return {
        "organization": ORGANIZATION_NAME,
        "job_title": JOB_TITLE,
        "total_resumes": total,
        "selected": selected,
        "interview": interview,
        "rejected": rejected
    }


# -----------------------------
# HEALTH CHECK
# -----------------------------
@app.get("/health")
def health():

    return {
        "status": "Healthy",
        "application": "HR AI Recruitment Agent",
        "version": "2.0"
    }


# -----------------------------
# ABOUT
# -----------------------------
@app.get("/about")
def about():

    return {
        "developer": "Rahib Siddiqui",
        "application": "HR AI Recruitment Agent",
        "features": [
            "Resume Upload",
            "PDF Parsing",
            "DOCX Parsing",
            "AI Resume Ranking",
            "AI Resume Scoring",
            "Top 10 Candidates",
            "Excel Report",
            "Dashboard",
            "Duplicate Detection"
        ]
    }
# ------------------------------
# DASHBOARD PAGE
# ------------------------------
@app.get("/dashboard-page",response_class=HTMLResponse)
def dashboard_page(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})
