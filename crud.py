from sqlalchemy.orm import Session

from models import Company, Candidate


# ==========================
# COMPANY CRUD
# ==========================

def create_company(db: Session, company):

    new_company = Company(
        organization_name=company.organization_name,
        job_title=company.job_title,
        required_skills=company.required_skills
    )

    db.add(new_company)
    db.commit()
    db.refresh(new_company)

    return new_company


def get_companies(db: Session):

    return db.query(Company).all()


# ==========================
# CANDIDATE CRUD
# ==========================

def create_candidate(db: Session, candidate):

    new_candidate = Candidate(

        file_name=candidate["file_name"],

        name=candidate["name"],

        email=candidate["email"],

        phone=candidate["phone"],

        age=candidate["age"],

        education=candidate["education"],

        experience=candidate["experience"],

        skills=", ".join(candidate["skills"]),

        ai_score=candidate["ai_score"],

        final_score=candidate["final_score"],

        recommendation=candidate["recommendation"],

        resume_text=candidate["text"]

    )

    db.add(new_candidate)
    db.commit()
    db.refresh(new_candidate)

    return new_candidate


def get_candidates(db: Session):

    return db.query(Candidate).all()


def get_candidate(db: Session, candidate_id: int):

    return db.query(Candidate).filter(
        Candidate.id == candidate_id
    ).first()


def delete_candidate(db: Session, candidate_id: int):

    candidate = db.query(Candidate).filter(
        Candidate.id == candidate_id
    ).first()

    if candidate:

        db.delete(candidate)

        db.commit()

        return True

    return False