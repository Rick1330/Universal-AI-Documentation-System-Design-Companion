from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
import shutil
import os

from app import crud, schemas # Corrected import
from app.db.session import get_db # Corrected import
from app.services import file_handler, job_orchestrator # Corrected import
from app.db.models import JobStatus # Corrected import
from app.core.logging_config import logger # Assuming logger is available here

router = APIRouter()

@router.post("/uploadfile/", response_model=schemas.job.JobSchema)
async def create_upload_file(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    if not file.filename:
        logger.error("File upload attempt with no filename.")
        raise HTTPException(status_code=400, detail="No filename provided")
    
    logger.info(f"Received file upload request for: {file.filename}")
    try:
        # Save file to a temporary local path first or directly to MinIO
        # For this example, let's assume file_handler saves it and returns a path/identifier
        # The file_handler.save_file_to_storage should be an async function
        stored_file_path = await file_handler.save_file_to_storage(file)
        logger.info(f"File 	'{file.filename}	' stored at: {stored_file_path}")

        # Create UploadedFile record
        uploaded_file_in = schemas.file.FileCreate(
            original_filename=file.filename,
            filename=os.path.basename(stored_file_path), # Or whatever unique name MinIO gives
            content_type=file.content_type,
            file_path=stored_file_path
        )
        db_uploaded_file = crud.file.create_uploaded_file(db=db, file_in=uploaded_file_in)
        logger.info(f"UploadedFile record created with ID: {db_uploaded_file.id}")

        # Create Job record
        job_in = schemas.job.JobCreate(uploaded_file_id=db_uploaded_file.id)
        db_job = crud.job.create_job(db=db, job_in=job_in)
        logger.info(f"Job record created with ID: {db_job.id}, status: {db_job.status}")

        # Trigger background processing task (e.g., Celery task)
        # For now, let's assume job_orchestrator.process_file_job is called
        # This call might be asynchronous or put into a task queue
        # job_orchestrator.process_file_job(job_id=db_job.id, db_provider=lambda: next(get_db()))
        # If process_file_job is async and we want to await it here (not typical for API endpoint)
        # await job_orchestrator.process_file_job(job_id=db_job.id, db_provider=lambda: next(get_db()))
        
        # For testing purposes, and if Celery is not fully set up for tests, 
        # we might call it directly or mock its call. The integration test does this.
        # In a real app, this would likely be: 
        # from app.workers.celery_app import process_file_job_task
        # process_file_job_task.delay(job_id=db_job.id)
        # For now, the integration test handles calling the orchestrator.
        # The API endpoint should just enqueue the job.
        
        # The integration test calls job_orchestrator.process_file_job directly.
        # For the API, we just create the job and it remains PENDING until a worker picks it up.
        # If we want to simulate the worker call for testing the API endpoint more deeply without full Celery:
        # This is tricky because get_db() is a generator. We need to pass a callable that provides a session.
        # For now, let's assume the job is created and the background task will be picked up.
        # The test_jobs_api.py already mocks process_file_job for the upload endpoint test.

        return db_job
    except Exception as e:
        logger.error(f"Error during file upload for 	'{file.filename}	': {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Could not process file: {str(e)}")

@router.get("/jobs/{job_id}", response_model=schemas.job.JobSchema)
def read_job(job_id: int, db: Session = Depends(get_db)):
    logger.info(f"Fetching job with ID: {job_id}")
    db_job = crud.job.get_job(db, job_id=job_id)
    if db_job is None:
        logger.warning(f"Job with ID: {job_id} not found.")
        raise HTTPException(status_code=404, detail="Job not found")
    logger.info(f"Job with ID: {job_id} found, status: {db_job.status}")
    return db_job

