from pydantic import BaseModel
from typing import Optional, Any
from datetime import datetime
from ..db.models import JobStatus # Assuming models.py is in ..db

# Schemas for UploadedFile
class UploadedFileBase(BaseModel):
    original_filename: Optional[str] = None
    content_type: Optional[str] = None

class UploadedFileCreate(UploadedFileBase):
    filename: str # Internal filename/key in object storage
    file_path: str

class UploadedFileInDBBase(UploadedFileBase):
    id: int
    filename: str
    file_path: str
    created_at: datetime

    class Config:
        orm_mode = True

class UploadedFileSchema(UploadedFileInDBBase):
    pass

# Schemas for Job
class JobBase(BaseModel):
    uploaded_file_id: Optional[int] = None

class JobCreate(JobBase):
    uploaded_file_id: int

class JobUpdate(BaseModel):
    status: Optional[JobStatus] = None
    results: Optional[Any] = None

class JobInDBBase(JobBase):
    id: int
    status: JobStatus
    created_at: datetime
    updated_at: Optional[datetime] = None
    results: Optional[Any] = None
    uploaded_file: Optional[UploadedFileSchema] = None # For response model

    class Config:
        orm_mode = True

class JobSchema(JobInDBBase):
    pass

class JobStatusResponse(BaseModel):
    job_id: int
    status: JobStatus
    message: Optional[str] = None
    results_summary: Optional[Any] = None # e.g. link to results or brief summary

