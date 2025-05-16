from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum as SAEnum
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import enum

Base = declarative_base()

class JobStatus(enum.Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"

class UploadedFile(Base):
    __tablename__ = "uploaded_files"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, index=True, nullable=False)
    filepath = Column(String, unique=True, nullable=False) # Could be S3 key or local path
    filetype = Column(String, nullable=True) # e.g., application/pdf, text/markdown
    filesize = Column(Integer, nullable=True) # in bytes
    upload_date = Column(DateTime, default=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationship to jobs (if a file is an input or output of a job)
    # These are illustrative; specific relationships might be defined on the Job model
    # jobs_as_input = relationship("Job", foreign_keys="[Job.input_file_id]")
    # jobs_as_output = relationship("Job", foreign_keys="[Job.output_file_id]")

class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    # type = Column(String, nullable=False) # e.g., "documentation_generation", "code_analysis"
    status = Column(SAEnum(JobStatus), default=JobStatus.PENDING, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    started_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)

    input_file_id = Column(Integer, ForeignKey("uploaded_files.id"), nullable=True)
    output_file_id = Column(Integer, ForeignKey("uploaded_files.id"), nullable=True)

    input_file = relationship("UploadedFile", foreign_keys=[input_file_id], backref="jobs_where_input")
    output_file = relationship("UploadedFile", foreign_keys=[output_file_id], backref="jobs_where_output")

    # Additional fields might include:
    # - user_id: ForeignKey to a users table
    # - config: JSONB or String to store job-specific configurations
    # - error_message: String to store error details if the job failed

# To initialize the database (e.g., in a main.py or a db_setup.py script):
# from sqlalchemy import create_engine
# from .config import DATABASE_URL # Assuming you have a config.py
# engine = create_engine(DATABASE_URL)
# Base.metadata.create_all(bind=engine)

