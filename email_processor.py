import os

from email_reader import get_unread_messages, fetch_email
from email_downloader import download_attachments

from parser import (
    extract_text_from_pdf,
    extract_text_from_docx,
    extract_candidate_info
)

from scoring import calculate_score
from ranking import rank_candidates
from excel_export import export_excel

from config import *


def process_emails():

    mail, email_ids = get_unread_messages()

    resumes = []

    for email_id in email_ids:

        msg, subject, sender = fetch_email(mail, email_id)

        files = download_attachments(msg)

        for filepath in files:

            extension = os.path.splitext(filepath)[1].lower()

            if extension == ".pdf":
                resume_text = extract_text_from_pdf(filepath)

            elif extension == ".docx":
                resume_text = extract_text_from_docx(filepath)

            else:
                continue

            info = extract_candidate_info(resume_text)

            candidate = {

                "file_name": os.path.basename(filepath),

                "name": info["name"],

                "email": info["email"],

                "phone": info["phone"],

                "skills": info["skills"],

                "experience": info["experience"],

                "age": info["age"],

                "education": info["education"],

                "text": resume_text

            }

            candidate["final_score"] = calculate_score(candidate)

            resumes.append(candidate)

    if len(resumes) == 0:

        return {
            "message": "No new resumes found"
        }

    top = rank_candidates(
        JOB_DESCRIPTION,
        resumes,
        TOP_CANDIDATES
    )

    filename = export_excel(
        top,
        ORGANIZATION_NAME,
        JOB_TITLE
    )

    return {
        "processed": len(resumes),
        "selected": len(top),
        "excel": filename
    }