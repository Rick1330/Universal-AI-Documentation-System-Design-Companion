# Development Plan: Phases and Tasks

This document outlines a phased development plan for the Universal Data Extractor + Analyzer. Each phase represents a significant milestone, delivering a subset of functionalities and building towards the full system. For each phase, suggested GitHub issues or tasks are listed to guide the development process.

## Phase 1: Core Backend Setup and Basic File Handling (MVP Foundation)

**Goal:** Establish the foundational backend infrastructure, including API services, database, object storage, and basic file upload/download capabilities. Implement the initial data flow for a single file type (e.g., TXT).

**Duration:** 2-3 Weeks

**Key Milestones:**
*   Backend project structure initialized.
*   Core services (File Ingestion, Job Management, basic AI Orchestration, Results) are set up with placeholder logic.
*   Database schema for jobs and basic file metadata defined.
*   Object storage integration for raw file uploads.
*   Basic asynchronous task processing with Celery and a message broker.
*   API endpoints for file upload and job status.

**Suggested GitHub Issues/Tasks:**

*   **Epic: Backend Foundation**
    *   `feat(backend): Initialize FastAPI project structure with Poetry/Pipenv` (#P1-T1)
    *   `feat(backend): Setup Dockerfile and docker-compose.yml for local development (FastAPI, PostgreSQL, Redis/RabbitMQ, MinIO)` (#P1-T2)
    *   `feat(db): Define initial PostgreSQL schema for 'jobs' and 'uploaded_files' tables using SQLAlchemy` (#P1-T3)
    *   `feat(backend/service): Implement File Ingestion Service - basic file validation (TXT) and storage to MinIO` (#P1-T4)
    *   `feat(backend/service): Implement Job Management Service - create job record, initial status update` (#P1-T5)
    *   `feat(backend/celery): Setup Celery with Redis/RabbitMQ; create a simple test task` (#P1-T6)
    *   `feat(backend/api): Create API endpoint for file upload (POST /files)` (#P1-T7)
    *   `feat(backend/api): Create API endpoint for job status retrieval (GET /jobs/{job_id})` (#P1-T8)
    *   `feat(backend/service): Implement basic AI Orchestration Service - placeholder for agent calls` (#P1-T9)
    *   `feat(backend/service): Implement basic Results Service - placeholder for result retrieval` (#P1-T10)
    *   `docs(backend): Document local development setup and core service interactions` (#P1-T11)

## Phase 2: MVP Data Extraction and Cleaning (TXT & CSV)

**Goal:** Implement the Data Extractor and Data Cleaner agents for TXT and CSV files. Integrate with LLM for basic text processing. Store and retrieve basic extracted/cleaned data.

**Duration:** 3-4 Weeks

**Key Milestones:**
*   Data Extractor Agent can process TXT files (full text) and CSV files (parse rows/columns).
*   Data Cleaner Agent can perform basic whitespace and numeric cleaning on TXT/CSV output.
*   LLM integration (e.g., OpenAI API via LangChain) for the Extractor Agent (e.g., identifying key-fields in TXT if simple patterns exist).
*   Results (extracted text, basic tables) are stored in PostgreSQL or Object Storage.
*   API can return basic extracted and cleaned data.

**Suggested GitHub Issues/Tasks:**

*   **Epic: MVP Extraction & Cleaning**
    *   `feat(backend/agent): Implement Data Extractor Agent - TXT file full text extraction` (#P2-T1)
    *   `feat(backend/agent): Implement Data Extractor Agent - CSV file parsing into tabular structure` (#P2-T2)
    *   `feat(backend/llm): Integrate LangChain with OpenAI API for basic LLM calls` (#P2-T3)
    *   `feat(backend/agent): Enhance Data Extractor Agent (TXT) to identify simple predefined key-fields using LLM` (#P2-T4)
    *   `feat(backend/agent): Implement Data Cleaner Agent - whitespace trimming for extracted data` (#P2-T5)
    *   `feat(backend/agent): Implement Data Cleaner Agent - basic numeric string cleaning (remove currency, commas)` (#P2-T6)
    *   `refactor(backend/celery): Create Celery task for TXT file processing pipeline (Extract -> Clean)` (#P2-T7)
    *   `refactor(backend/celery): Create Celery task for CSV file processing pipeline (Extract -> Clean)` (#P2-T8)
    *   `feat(backend/db): Design schema/method for storing extracted text and simple tables` (#P2-T9)
    *   `feat(backend/api): Enhance Results Service and API endpoint to return cleaned TXT/CSV data` (#P2-T10)
    *   `test(backend): Add unit tests for TXT and CSV extraction and cleaning logic` (#P2-T11)

## Phase 3: MVP Data Analysis and PDF Processing

**Goal:** Implement the Data Analyzer Agent for basic text summarization, keyword extraction, and descriptive stats. Add PDF file support (text and simple table extraction).

**Duration:** 3-4 Weeks

**Key Milestones:**
*   Data Extractor Agent can process PDF files (extract text, attempt simple table extraction using PyMuPDF/Camelot).
*   Data Analyzer Agent can generate text summaries and keywords using LLM.
*   Data Analyzer Agent can calculate descriptive statistics for cleaned tabular data.
*   Results include analysis outputs.

**Suggested GitHub Issues/Tasks:**

*   **Epic: MVP Analysis & PDF Support**
    *   `feat(backend/agent): Implement Data Extractor Agent - PDF text extraction using PyMuPDF` (#P3-T1)
    *   `feat(backend/agent): Implement Data Extractor Agent - PDF simple table extraction (e.g., using Camelot or LLM vision if feasible)` (#P3-T2)
    *   `feat(backend/agent): Implement Data Analyzer Agent - text summarization using LLM` (#P3-T3)
    *   `feat(backend/agent): Implement Data Analyzer Agent - keyword extraction from text using LLM/NLTK` (#P3-T4)
    *   `feat(backend/agent): Implement Data Analyzer Agent - descriptive statistics for numeric columns in tables` (#P3-T5)
    *   `refactor(backend/celery): Create Celery task for PDF file processing pipeline (Extract -> Clean -> Analyze)` (#P3-T6)
    *   `feat(backend/api): Enhance Results Service and API to include analysis outputs (summary, keywords, stats)` (#P3-T7)
    *   `test(backend): Add unit tests for PDF processing and basic analysis features` (#P3-T8)
    *   `docs(prompts): Refine and version control prompts for Extractor, Cleaner, Analyzer based on initial tests` (#P3-T9)

## Phase 4: MVP Frontend Development (Lovable.dev)

**Goal:** Develop the MVP frontend using Lovable.dev, allowing users to upload files (TXT, CSV, PDF), view processing status, and see extracted data, basic analysis, and a simple chart.

**Duration:** 4-5 Weeks

**Key Milestones:**
*   Lovable.dev project setup.
*   File upload page implemented.
*   Processing status display.
*   Results page with tabs for overview/summary, extracted data (text, key-fields, tables), and analysis (stats, basic chart).
*   Download extracted data as CSV functionality.

**Suggested GitHub Issues/Tasks:**

*   **Epic: MVP Frontend**
    *   `feat(frontend): Setup Lovable.dev project structure and basic layout/navigation` (#P4-T1)
    *   `feat(frontend): Implement FileUploadComponent for TXT, CSV, PDF with client-side validation` (#P4-T2)
    *   `feat(frontend): Implement UploadPage - integrate FileUploadComponent, call backend upload API` (#P4-T3)
    *   `feat(frontend): Implement job status polling and ProcessingIndicatorComponent` (#P4-T4)
    *   `feat(frontend): Implement ResultsPage layout with tab navigation (Overview, Extracted Data, Analysis)` (#P4-T5)
    *   `feat(frontend/results): Implement Overview tab - display summary, keywords, overall insights` (#P4-T6)
    *   `feat(frontend/results): Implement Extracted Data tab - TextViewer, KeyValueDisplay, DataTableComponent` (#P4-T7)
    *   `feat(frontend/results): Implement Analysis tab - StatsDisplay, basic ChartComponent (bar chart)` (#P4-T8)
    *   `feat(frontend): Implement DownloadButtonComponent and CSV export functionality` (#P4-T9)
    *   `test(frontend): Basic UI tests for MVP features` (#P4-T10)
    *   `docs(frontend): Document Lovable.dev component structure and API interactions` (#P4-T11)

## Phase 5: Iteration 1 - Stretch Goals (e.g., Image/DOCX Support, Advanced Cleaning)

**Goal:** Begin implementing high-priority stretch goals, such as support for image files (with OCR) and DOCX files, and more advanced data cleaning options.

**Duration:** 4-6 Weeks

**Key Milestones:**
*   Data Extractor Agent supports image (JPG, PNG) input with Tesseract OCR.
*   Data Extractor Agent supports DOCX file input.
*   Data Cleaner Agent includes more advanced normalization (e.g., data type inference, unit standardization for common cases).
*   Refinement of existing features based on initial testing/feedback.

**Suggested GitHub Issues/Tasks:**

*   **Epic: Stretch Goals - Iteration 1**
    *   `feat(backend/ocr): Integrate Tesseract OCR for image-to-text conversion` (#P5-T1)
    *   `feat(backend/agent): Enhance Data Extractor to handle image inputs (JPG, PNG) via OCR` (#P5-T2)
    *   `feat(backend/agent): Enhance Data Extractor to handle DOCX file input using python-docx` (#P5-T3)
    *   `feat(backend/agent): Enhance Data Cleaner with basic data type inference (numeric, date)` (#P5-T4)
    *   `feat(backend/agent): Enhance Data Cleaner with contextual unit standardization (e.g., common currencies)` (#P5-T5)
    *   `refactor(backend/celery): Update Celery tasks for new file types and cleaning steps` (#P5-T6)
    *   `test(backend): Add tests for image and DOCX processing, advanced cleaning` (#P5-T7)
    *   `feat(frontend): Update file upload component to accept JPG, PNG, DOCX` (#P5-T8)
    *   `chore: Conduct internal review and gather feedback on MVP for refinement` (#P5-T9)

## Phase 6: Iteration 2 - Stretch Goals (e.g., Advanced Analysis, UI Enhancements)

**Goal:** Implement more advanced analytical features and enhance the user interface based on feedback and priorities.

**Duration:** 4-6 Weeks

**Key Milestones:**
*   Data Analyzer Agent includes features like basic sentiment analysis (for text) or trend identification (for time-series data if applicable).
*   UI/UX improvements: interactive data correction (basic), more chart types.
*   User authentication and basic account management (if prioritized).

**Suggested GitHub Issues/Tasks:**

*   **Epic: Stretch Goals - Iteration 2**
    *   `feat(backend/agent): Enhance Data Analyzer with basic sentiment analysis for extracted text` (#P6-T1)
    *   `feat(backend/agent): Enhance Data Analyzer with simple trend detection for tabular time-series data` (#P6-T2)
    *   `feat(frontend/results): Implement basic interactive data correction for key-fields or table cells` (#P6-T3)
    *   `feat(frontend/results): Add support for 1-2 additional chart types in ChartComponent` (#P6-T4)
    *   `feat(backend): Implement basic user authentication (e.g., JWT-based)` (#P6-T5)
    *   `feat(frontend): Implement login/registration pages and integrate with auth API` (#P6-T6)
    *   `docs: Update all documentation to reflect new features and changes` (#P6-T7)

## Ongoing Activities (Across all Phases):

*   `chore: Regular code reviews and adherence to coding standards`
*   `chore: Continuous integration and automated testing (GitHub Actions)`
*   `chore: Dependency management and security vulnerability scanning`
*   `docs: Keep all documentation (READMEs, technical docs, prompts) updated with changes`
*   `bug: Address bugs and issues identified during testing or feedback`

This phased plan allows for iterative development, regular delivery of value, and flexibility to adapt to new requirements or priorities. Each phase should conclude with a review and planning session for the next phase.
