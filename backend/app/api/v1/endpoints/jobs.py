from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, BackgroundTasks
from sqlalchemy.orm import Session
from typing import Any
import shutil
import uuid
import os

from ....app import schemas # Dotted path from endpoints directory
from ....app import crud # Dotted path from endpoints directory
from ....app.db import session as db_session # Dotted path from endpoints directory
from ....app.core.config import settings
from ....app.services import file_handler, job_orchestrator # Dotted path from endpoints directory

router = APIRouter()

@router.post("/uploadfile/", response_model=schemas.job.JobSchema)
async def create_upload_file(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    db: Session = Depends(db_session.get_db)
) -> Any:
    """
    Upload a file for processing.
    """
    if not file.filename:
        raise HTTPException(status_code=400, detail="No filename provided")

    # Generate a unique filename to avoid collisions
    unique_id = uuid.uuid4()
    file_extension = os.path.splitext(file.filename)[1]
    internal_filename = f"{unique_id}{file_extension}"

    try:
        # Store the file temporarily locally before uploading to MinIO
        # In a production system, you might stream directly or use a more robust temp storage
        temp_file_path = f"/tmp/{internal_filename}"
        with open(temp_file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Upload to MinIO (or other object storage)
        file_path_in_storage = await file_handler.save_file_to_storage(temp_file_path, internal_filename, file.content_type)
        os.remove(temp_file_path) # Clean up temp file

    except Exception as e:
        # Clean up temp file if it exists and an error occurs
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)
        raise HTTPException(status_code=500, detail=f"Could not save file: {e}")
    finally:
        file.file.close()

    db_file = crud.file.create_uploaded_file(
        db=db, 
        file_in=schemas.file.UploadedFileCreate(
            filename=internal_filename, 
            original_filename=file.filename,
            content_type=file.content_type,
            file_path=file_path_in_storage
            )
        )
    
    if not db_file:
        raise HTTPException(status_code=500, detail="Could not record file in database.")

    # Create a job for this file
    job_in = schemas.job.JobCreate(uploaded_file_id=db_file.id)
    db_job = crud.job.create_job(db=db, job_in=job_in)

    if not db_job:
        # Potentially delete the file from storage and db if job creation fails, or mark as orphaned
        raise HTTPException(status_code=500, detail="Could not create processing job.")

    # Add the processing task to background tasks
    background_tasks.add_task(job_orchestrator.process_file_job, job_id=db_job.id, db_provider=db_session.get_db)
    
    return db_job


@router.get("/jobs/{job_id}", response_model=schemas.job.JobSchema)
def read_job(
    job_id: int,
    db: Session = Depends(db_session.get_db)
) -> Any:
    """
    Retrieve job status and results.
    """
    db_job = crud.job.get_job(db, job_id=job_id)
    if db_job is None:
        raise HTTPException(status_code=404, detail="Job not found")
    return db_job

