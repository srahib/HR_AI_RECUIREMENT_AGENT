from config import *


def calculate_score(candidate):
    score = 0

    # ----------------------------
    # Skills (40 Marks)
    # ----------------------------
    matched_skills = len(candidate["skills"])

    if len(REQUIRED_SKILLS) > 0:
        score += (matched_skills / len(REQUIRED_SKILLS)) * 40

    # ----------------------------
    # Experience (30 Marks)
    # ----------------------------
    experience = candidate["experience"]

    if experience >= MIN_EXPERIENCE:
        score += 30
    elif MIN_EXPERIENCE > 0:
        score += (experience / MIN_EXPERIENCE) * 30

    # ----------------------------
    # Age (10 Marks)
    # ----------------------------
    if candidate["age"] is not None:
        if MIN_AGE <= candidate["age"] <= MAX_AGE:
            score += 10

    # ----------------------------
    # Education (10 Marks)
    # ----------------------------
    if candidate["education"] != "Unknown":
        score += 10

    # ----------------------------
    # Email (5 Marks)
    # ----------------------------
    if candidate["email"]:
        score += 5

    # ----------------------------
    # Phone (5 Marks)
    # ----------------------------
    if candidate["phone"]:
        score += 5

    return round(score, 2)


def get_recommendation(score):

    if score >= 80:
        return "Selected"

    elif score >= 60:
        return "Interview"

    else:
        return "Rejected"

