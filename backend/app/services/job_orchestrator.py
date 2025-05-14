from sqlalchemy.orm import Session
from typing import Callable
import os

from app import crud # Corrected import
from app.db import models # Corrected import
from app.core.config import settings # Corrected import
from app.services import file_handler # Corrected import
from app.services.ai_agents import extractor_agent, cleaner_agent, analyzer_agent # Corrected import

# from app.workers.celery_app import celery_app # Placeholder for Celery integration

# @celery_app.task # This would be uncommented if Celery is fully set up
async def process_file_job(job_id: int, db_provider: Callable[[], Session]):
    """
    Background task to process a file associated with a job.
    This function will be called by Celery or a similar background task runner.
    db_provider is a callable that yields a new DB session.
    """
    db = next(db_provider()) # Get a new DB session for this task
    local_file_path = None # Initialize to ensure it's defined for finally block
    try:
        job = crud.job.get_job(db, job_id=job_id)
        if not job or not job.uploaded_file:
            print(f"Job or uploaded file not found for job_id: {job_id}")
            if job:
                crud.job.update_job_status(db, job_id=job_id, status=models.JobStatus.FAILED)
                crud.job.update_job_results(db, job_id=job_id, results={"error": "Job or uploaded file not found"})
            return

        crud.job.update_job_status(db, job_id=job_id, status=models.JobStatus.PROCESSING)
        print(f"Processing job_id: {job_id} for file: {job.uploaded_file.original_filename}")

        # 1. Get file from storage
        temp_dir = "/tmp/universal_data_extractor"
        os.makedirs(temp_dir, exist_ok=True)
        local_file_path = os.path.join(temp_dir, job.uploaded_file.filename)
        
        await file_handler.get_file_from_storage(job.uploaded_file.file_path, local_file_path)
        print(f"File {job.uploaded_file.filename} downloaded to {local_file_path} for processing.")

        # 2. Run Extractor Agent
        extracted_data = await extractor_agent.run_extraction_agent(
            local_file_path, 
            job.uploaded_file.content_type, 
            job.uploaded_file.original_filename
        )
        print(f"Extraction complete for job_id: {job_id}")

        # 3. Run Cleaner Agent
        cleaned_data = await cleaner_agent.run_cleaning_agent(extracted_data)
        print(f"Cleaning complete for job_id: {job_id}")

        # 4. Run Analyzer Agent
        analysis_results = await analyzer_agent.run_analysis_agent(cleaned_data)
        print(f"Analysis complete for job_id: {job_id}")

        # 5. Store results
        final_results = {
            "extraction": extracted_data,
            "cleaning": cleaned_data, # Optional: could be merged or just keep final analysis
            "analysis": analysis_results
        }
        crud.job.update_job_results(db, job_id=job_id, results=final_results)
        crud.job.update_job_status(db, job_id=job_id, status=models.JobStatus.COMPLETED)
        print(f"Job {job_id} completed successfully.")

    except Exception as e:
        print(f"Error processing job {job_id}: {e}")
        # Ensure job status is updated even if it was already FAILED by a sub-component
        crud.job.update_job_status(db, job_id=job_id, status=models.JobStatus.FAILED)
        error_details = {"error": str(e), "step": "job_orchestration"}
        # Append to existing results if any, or create new
        existing_results = job.results if job and job.results else {}
        if isinstance(existing_results, dict):
            existing_results.update(error_details) # Merge error into existing results
            crud.job.update_job_results(db, job_id=job_id, results=existing_results)
        else: # If results is not a dict (e.g. a list or string), overwrite with error
            crud.job.update_job_results(db, job_id=job_id, results=error_details)
        
    finally:
        if local_file_path and os.path.exists(local_file_path):
            try:
                os.remove(local_file_path) # Clean up downloaded file
                print(f"Cleaned up temporary file: {local_file_path}")
            except OSError as e_remove:
                print(f"Error removing temporary file {local_file_path}: {e_remove}")
        db.close()

