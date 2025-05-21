// API service for interacting with backend
import { ApiError, FileUploadRequest, FileUploadResponse, Job } from "../types";

// API base URL
const API_BASE_URL = "/api/v1"; // Assuming the backend is served on the same domain or proxied

// Helper function to handle API responses
async function handleResponse<T>(response: Response): Promise<T> {
  if (!response.ok) {
    let errorData: ApiError | { detail: string } | string = { detail: `HTTP error! status: ${response.status}` };
    try {
      errorData = await response.json();
    } catch (e) {
      // If parsing JSON fails, use the status text or a generic message
      errorData = { detail: response.statusText || `HTTP error! status: ${response.status}` };
    }

    // Ensure errorData has a 'detail' property for consistency, 
    // or construct one if it's a simple string.
    let errorMessage = "An unknown error occurred";
    if (typeof errorData === "string") {
      errorMessage = errorData;
    } else if (errorData && typeof errorData === "object" && "detail" in errorData) {
      errorMessage = (errorData as { detail: string }).detail;
    } else if (response.statusText) {
      errorMessage = response.statusText;
    }
    
    const error: ApiError = { detail: errorMessage };
    throw error;
  }
  return response.json() as Promise<T>;
}

export const uploadFile = async (request: FileUploadRequest): Promise<FileUploadResponse> => {
  const formData = new FormData();
  formData.append("file", request.file);

  const response = await fetch(`${API_BASE_URL}/jobs/`, {
    method: "POST",
    body: formData,
    // Headers are not explicitly set for FormData; the browser will set Content-Type to multipart/form-data with the correct boundary.
  });

  return handleResponse<FileUploadResponse>(response);
};

export const getJobStatus = async (jobId: string): Promise<Job> => {
  const response = await fetch(`${API_BASE_URL}/jobs/${jobId}`, {
    method: "GET",
    headers: {
      "Accept": "application/json",
    },
  });
  return handleResponse<Job>(response);
};

export const getAllJobs = async (): Promise<Job[]> => {
  const response = await fetch(`${API_BASE_URL}/jobs/`, {
    method: "GET",
    headers: {
      "Accept": "application/json",
    },
  });
  return handleResponse<Job[]>(response);
};

