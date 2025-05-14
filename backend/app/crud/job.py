from sqlalchemy.orm import Session
from ..db import models
from ..schemas import job as job_schema # Renamed to avoid conflict
from ..db.models import JobStatus
from typing import Any

def get_job(db: Session, job_id: int):
    return db.query(models.Job).filter(models.Job.id == job_id).first()

def create_job(db: Session, job_in: job_schema.JobCreate):
    db_job = models.Job(
        uploaded_file_id=job_in.uploaded_file_id,
        status=JobStatus.PENDING
    )
    db.add(db_job)
    db.commit()
    db.refresh(db_job)
    return db_job

def update_job_status(db: Session, job_id: int, status: JobStatus):
    db_job = get_job(db, job_id)
    if db_job:
        db_job.status = status
        db.commit()
        db.refresh(db_job)
    return db_job

def update_job_results(db: Session, job_id: int, results: Any):
    db_job = get_job(db, job_id)
    if db_job:
        db_job.results = results
        db.commit()
        db.refresh(db_job)
    return db_job

def update_job(db: Session, job_id: int, job_in: job_schema.JobUpdate):
    db_job = get_job(db, job_id)
    if not db_job:
        return None
    
    update_data = job_in.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_job, key, value)
    
    db.add(db_job)
    db.commit()
    db.refresh(db_job)
    return db_job

