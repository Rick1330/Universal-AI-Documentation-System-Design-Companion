from fastapi import APIRouter
from .endpoints import jobs # Corrected relative import

api_router = APIRouter()
api_router.include_router(jobs.router, prefix="/jobs", tags=["jobs"])

