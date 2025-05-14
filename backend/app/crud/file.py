from sqlalchemy.orm import Session
from ..db import models
from ..schemas import file as file_schema # Renamed to avoid conflict


def get_uploaded_file(db: Session, file_id: int):
    return db.query(models.UploadedFile).filter(models.UploadedFile.id == file_id).first()

def create_uploaded_file(db: Session, file_in: file_schema.UploadedFileCreate):
    db_file = models.UploadedFile(
        filename=file_in.filename,
        original_filename=file_in.original_filename,
        content_type=file_in.content_type,
        file_path=file_in.file_path
    )
    db.add(db_file)
    db.commit()
    db.refresh(db_file)
    return db_file

