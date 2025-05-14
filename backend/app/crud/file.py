from sqlalchemy.orm import Session
from app.db import models
from app.schemas.file import UploadedFileCreate # Corrected import

def create_uploaded_file(db: Session, *, file_in: UploadedFileCreate) -> models.UploadedFile:
    db_file = models.UploadedFile(**file_in.model_dump())
    db.add(db_file)
    db.commit()
    db.refresh(db_file)
    return db_file

def get_uploaded_file(db: Session, file_id: int) -> models.UploadedFile | None:
    return db.query(models.UploadedFile).filter(models.UploadedFile.id == file_id).first()

# Add other CRUD operations for UploadedFile if needed (e.g., list, delete)

