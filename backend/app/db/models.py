import enum
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, JSON, Enum as SQLEnum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..db.base import Base

class JobStatus(str, enum.Enum):
    PENDING = "PENDING"
    PROCESSING = "PROCESSING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"

class UploadedFile(Base):
    __tablename__ = "uploaded_files"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, index=True)
    original_filename = Column(String)
    content_type = Column(String)
    file_path = Column(String)  # Path in MinIO/Object Storage
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    job = relationship("Job", back_populates="uploaded_file", uselist=False)

class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    uploaded_file_id = Column(Integer, ForeignKey("uploaded_files.id"))
    status = Column(SQLEnum(JobStatus), default=JobStatus.PENDING)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    results = Column(JSON)  # To store extracted data, analysis, etc.

    uploaded_file = relationship("UploadedFile", back_populates="job")

