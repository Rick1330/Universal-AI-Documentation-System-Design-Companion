# Use an official Python runtime as a parent image
FROM python:3.11-slim as builder

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /app

# Install Poetry
RUN pip install --no-cache-dir poetry==1.8.2 # Using a specific version for consistency

# Copy only requirements to cache them in docker layer
COPY backend/pyproject.toml backend/poetry.lock* ./

# Install project dependencies
# --no-root: Do not install the project itself, only dependencies
# --no-dev: Exclude development dependencies if you have them and don't need them in production image
RUN poetry install --no-root --no-interaction --no-ansi

# Create a new stage for the final image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

# Copy installed dependencies from the builder stage
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /app/pyproject.toml /app/poetry.lock* /app/

# Copy the project files
COPY backend/app /app/app
COPY backend/README.md /app/

# Install the project itself using poetry (needed if it's a package)
# RUN poetry install --no-interaction --no-ansi --only-main
# For this simple structure, we might not need to install the project if main.py is run directly.
# However, to ensure poetry environment is fully utilized for running:
RUN pip install --no-cache-dir poetry==1.8.2 && poetry install --no-interaction --no-ansi --only main

# Expose port 8000
EXPOSE 8000

# Command to run the application
CMD ["poetry", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

