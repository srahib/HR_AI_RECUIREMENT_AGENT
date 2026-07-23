import re
import pdfplumber
from docx import Document
from config import REQUIRED_SKILLS, REQUIRED_EDUCATION


# -----------------------------
# PDF TEXT EXTRACTION
# -----------------------------
def extract_text_from_pdf(pdf_path):

    text = ""

    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()

                if page_text:
                    text += page_text + "\n"

    except Exception as e:
        print(e)

    return text


# -----------------------------
# DOCX TEXT EXTRACTION
# -----------------------------
def extract_text_from_docx(docx_path):

    text = ""

    try:
        doc = Document(docx_path)

        for para in doc.paragraphs:
            text += para.text + "\n"

    except Exception as e:
        print(e)

    return text


# -----------------------------
# CANDIDATE INFO EXTRACTION
# -----------------------------
def extract_candidate_info(text):

    email_pattern = r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"
    phone_pattern = r"(?:\+92|0)3\d{9}"

    emails = re.findall(email_pattern, text)
    phones = re.findall(phone_pattern, text)

    # Skills
    found_skills = []

    for skill in REQUIRED_SKILLS:
        if skill.lower() in text.lower():
            found_skills.append(skill)

    # Experience
    experience = 0

    exp_match = re.search(r"(\d+)\s*(year|years)", text.lower())

    if exp_match:
        experience = int(exp_match.group(1))

    # Age
    age = None

    age_match = re.search(r"Age[:\s]*(\d{2})", text, re.IGNORECASE)

    if age_match:
        age = int(age_match.group(1))

    # Education
    education = "Unknown"

    for edu in REQUIRED_EDUCATION:
        if edu.lower() in text.lower():
            education = edu
            break

    # Name
    name = "Unknown"

    lines = text.split("\n")

    for line in lines:

        line = line.strip()

        if len(line) > 3 and len(line.split()) <= 4:

            if "@" not in line:
                name = line
                break

    return {
        "name": name,
        "email": emails[0] if emails else "",
        "phone": phones[0] if phones else "",
        "skills": found_skills,
        "experience": experience,
        "age": age,
        "education": education
    }