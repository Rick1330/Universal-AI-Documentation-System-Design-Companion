from fastapi import APIRouter

from ....app.api.v1.endpoints import jobs # Dotted path from v1 directory

api_router = APIRouter()
api_router.include_router(jobs.router, prefix="/jobs", tags=["jobs"])
# The prefix /jobs was already in jobs.py, so we use it here for consistency
# Or, we can remove prefix from jobs.router and define it here as /jobs or /files for upload
# For now, let's assume /api/v1/jobs/uploadfile/ and /api/v1/jobs/jobs/{job_id}
# Let's adjust jobs.py to have a more logical prefix for the router itself.

# Re-evaluating the jobs.py, the router is defined there without a prefix.
# The current structure in jobs.py is @router.post("/uploadfile/") and @router.get("/jobs/{job_id}")
# This means the full paths would be /api/v1/uploadfile/ and /api/v1/jobs/{job_id}
# This is a bit inconsistent. Let's make the jobs router handle all job-related things under /jobs
# and create a new router for file uploads under /files.

# For now, sticking to the user's current file structure for jobs.py which includes uploadfile
# So the path will be /api/v1/jobs/uploadfile/ and /api/v1/jobs/jobs/{job_id}
# This is fine for now, can be refactored later if needed.

