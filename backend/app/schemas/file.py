from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# Schemas for UploadedFile
class UploadedFileBase(BaseModel):
    original_filename: Optional[str] = None
    content_type: Optional[str] = None

class UploadedFileCreate(UploadedFileBase):
    filename: str # Internal filename/key in object storage
    file_path: str
    original_filename: str
    content_type: str

class UploadedFileInDBBase(UploadedFileBase):
    id: int
    filename: str
    file_path: str
    created_at: datetime

    class Config:
        orm_mode = True

class UploadedFileSchema(UploadedFileInDBBase):
    pass

