# GitHub Repository Layout

An optimal GitHub repository structure is essential for maintainability, scalability, and collaboration for the Universal Data Extractor + Analyzer project. The proposed layout emphasizes a clear separation of concerns, particularly between the frontend and backend, and provides dedicated directories for documentation, AI prompts, configuration files, and sample data.

This structure is designed to support both individual developers and larger teams, facilitating independent work on different components while maintaining a cohesive project organization.

## Proposed Folder Structure

```
universal-data-extractor-analyzer/
├── .github/                    # GitHub-specific files (workflows, issue templates)
│   └── workflows/              # CI/CD pipelines (e.g., build, test, deploy)
│       └── main.yml
├── backend/                    # All backend-related code and services
│   ├── app/                    # Main application code for FastAPI services
│   │   ├── __init__.py
│   │   ├── api/                # API endpoint definitions (routers)
│   │   │   ├── __init__.py
│   │   │   ├── v1/             # API version 1
│   │   │   │   ├── __init__.py
│   │   │   │   ├── endpoints/  # Specific endpoint modules
│   │   │   │   │   ├── __init__.py
│   │   │   │   │   ├── files.py
│   │   │   │   │   └── jobs.py
│   │   │   │   └── router.py   # Main router for v1
│   │   ├── core/               # Core logic, configuration, settings
│   │   │   ├── __init__.py
│   │   │   └── config.py
│   │   ├── crud/               # Create, Read, Update, Delete operations (database interactions)
│   │   │   └── __init__.py
│   │   ├── db/                 # Database models, session management (SQLAlchemy)
│   │   │   ├── __init__.py
│   │   │   ├── base.py
│   │   │   └── models.py
│   │   ├── schemas/            # Pydantic schemas for data validation and serialization
│   │   │   └── __init__.py
│   │   ├── services/           # Business logic for services (File Ingestion, Job Mgmt, AI Orchestration)
│   │   │   ├── __init__.py
│   │   │   ├── ai_orchestrator.py
│   │   │   └── file_handler.py
│   │   └── main.py             # FastAPI application entry point
│   ├── workers/                # Celery worker definitions and tasks
│   │   ├── __init__.py
│   │   ├── celery_app.py       # Celery application instance
│   │   └── tasks/              # Specific task modules (extraction, cleaning, analysis)
│   │       ├── __init__.py
│   │       ├── extraction_tasks.py
│   │       ├── cleaning_tasks.py
│   │       └── analysis_tasks.py
│   ├── tests/                  # Backend unit and integration tests
│   │   └── ... 
│   ├── Dockerfile              # Dockerfile for building the backend service
│   ├── requirements.txt        # Python dependencies for the backend
│   └── celery_worker_entrypoint.sh # Script to start Celery workers
├── frontend/                   # All frontend-related code (Lovable.dev project)
│   ├── lovable-project/        # Root of the Lovable.dev project export/structure
│   │   ├── components/         # Reusable UI components
│   │   ├── pages/              # Different pages/views of the application
│   │   ├── assets/             # Static assets (images, fonts specific to frontend)
│   │   ├── services/           # Frontend services for API calls
│   │   ├── store/              # State management (if applicable)
│   │   └── ...                 # Other Lovable.dev specific files and folders
│   ├── Dockerfile              # Optional: Dockerfile for building/serving the frontend if needed
│   └── README.md               # Frontend specific setup and development guide
├── docs/                       # All project documentation
│   ├── system-overview.md      # High-level technical description (already created)
│   ├── architecture.md         # System components, interactions (already created)
│   ├── api-reference.md        # (Optional) Detailed API endpoint documentation (e.g., generated from OpenAPI spec)
│   ├── usage-examples.md       # (Optional) Examples of how to use the system/API
│   └── environment-setup.md    # (Optional) Guide for setting up development environment
├── prompts/                    # AI agent prompts
│   ├── extractor.md            # Prompt for Data Extractor Agent (already created)
│   ├── cleaner.md              # Prompt for Data Cleaner Agent (already created)
│   ├── analyzer.md             # Prompt for Data Analyzer Agent (already created)
│   └── README.md               # Explanation of how prompts are used/structured
├── data/                       # Sample data, test files, (NOT for user production data)
│   ├── samples/                # Example files for testing (PDFs, CSVs, images)
│   └── test_outputs/           # Expected outputs for test cases (if applicable)
├── config/                     # Configuration files (e.g., for services, LLM keys - use .env for secrets)
│   ├── settings.yaml           # General application settings (non-sensitive)
│   └── logging.conf            # Logging configuration
├── scripts/                    # Utility scripts (e.g., deployment, data migration, cron jobs)
│   ├── deploy.sh
│   └── run_dev_server.sh
├── .dockerignore               # Specifies intentionally untracked files for Docker builds
├── .env.example                # Example environment variables file (for secrets, API keys - DO NOT COMMIT .env)
├── .gitignore                  # Specifies intentionally untracked files that Git should ignore
├── docker-compose.yml          # Docker Compose file for local development setup (backend, db, broker, object storage)
├── LICENSE                     # Project license file (e.g., MIT, Apache 2.0)
└── README.md                   # Main project README (public-facing, professional introduction - already created)
```

### Explanation of Key Directories:

*   **`.github/`**: Contains GitHub-specific configurations, primarily for CI/CD workflows using GitHub Actions. This ensures automated testing and deployment processes.
*   **`backend/`**: A self-contained directory for all backend Python code. It follows a standard FastAPI project structure with clear separation for API endpoints (`api`), core logic (`core`), database interactions (`crud`, `db`), data schemas (`schemas`), business logic services (`services`), and the main application entry point (`main.py`). Celery workers and their tasks are also organized here (`workers`).
*   **`frontend/`**: Houses the Lovable.dev project. The `lovable-project/` subdirectory would ideally mirror the structure exported or maintained by Lovable.dev, ensuring that frontend development can proceed independently.
*   **`docs/`**: Central location for all project documentation beyond the main README. This includes detailed system architecture, API references (potentially auto-generated), and setup guides.
*   **`prompts/`**: Stores the detailed prompts used to guide the Large Language Models (LLMs) for the different AI agents. This separation makes it easy to manage, version, and refine prompts.
*   **`data/`**: Intended for sample files used during development and testing, or for small, static datasets. This directory should **not** be used for storing user-uploaded production data, which will reside in Object Storage.
*   **`config/`**: Contains non-sensitive configuration files. Sensitive configurations like API keys should be managed through environment variables (e.g., via a `.env` file that is not committed to the repository, with `.env.example` as a template).
*   **`scripts/`**: For helper scripts that automate common development or operational tasks.
*   **Root Directory Files:** Includes essential project files like `docker-compose.yml` for local development orchestration, `.gitignore`, `LICENSE`, and the main `README.md`.

### Benefits of this Structure:

*   **Modularity:** Clear separation between frontend, backend, documentation, and other concerns allows teams to work on different parts of the system with minimal interference.
*   **Scalability:** The backend structure is designed to accommodate growth, allowing for the addition of new API versions, services, or worker tasks in an organized manner.
*   **Maintainability:** A consistent and logical structure makes it easier for developers to understand the codebase, locate files, and make changes.
*   **Collaboration:** Well-defined boundaries simplify collaboration, as different developers or teams can own specific directories or components.
*   **CI/CD Friendly:** The structure supports automated build, test, and deployment processes, especially with the `.github/workflows` directory.
*   **Onboarding:** New developers can more quickly get up to speed with the project layout and conventions.

This proposed GitHub repository layout provides a robust and professional foundation for the Universal Data Extractor + Analyzer project, aligning with best practices for modern software development.
