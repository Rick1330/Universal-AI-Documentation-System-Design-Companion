# System Architecture: Universal Data Extractor + Analyzer

## 1. Introduction

This document provides a detailed description of the system architecture for the Universal Data Extractor + Analyzer. It outlines the core components, their interactions, data flows, the roles and orchestration of AI agents, and the key technologies and libraries that underpin the system. The architecture is designed to be modular, scalable, and robust, supporting both the Minimum Viable Product (MVP) functionalities and future stretch goals.

## 2. Overall System Architecture

The Universal Data Extractor + Analyzer is designed as a modular, microservices-oriented architecture to ensure scalability, maintainability, and flexibility. This approach allows individual components to be developed, deployed, and scaled independently.

### 2.1. Core System Components

The system comprises the following primary components:

1.  **Frontend (Client Application):**
    *   **Description:** The user-facing interface, built with Lovable.dev. It is responsible for handling user interactions, file uploads, displaying extracted data and analysis results, and rendering visualizations.
    *   **Key Functions:** User authentication (stretch goal), file selection and upload, job status monitoring, results display (text, tables, charts), user input for analysis parameters (stretch goal).

2.  **API Gateway:**
    *   **Description:** A single entry point for all client requests. It routes requests to the appropriate backend services, handles authentication and authorization (stretch goal), rate limiting, and request/response transformations.
    *   **Technology:** Can be built using FastAPI itself or a dedicated gateway solution like Kong, Tyk, or cloud provider gateways.

3.  **Backend Services (FastAPI):**
    *   **a. File Ingestion Service:** Handles incoming file uploads, validates them, stores raw files in Object Storage, and creates initial job records.
    *   **b. Job Management Service:** Manages the lifecycle of data processing jobs, dispatches tasks to asynchronous workers, and tracks job statuses.
    *   **c. AI Orchestration Service (Agent Controller):** Coordinates the sequence of AI agent operations (Extractor, Cleaner, Analyzer), interacts with LLMs and specialized libraries, and manages data flow between agents.
    *   **d. Results Service:** Provides processed and analyzed data to the frontend, fetching results from data stores.

4.  **Asynchronous Task Workers (Celery):**
    *   **Description:** A pool of background workers that execute long-running tasks (file parsing, OCR, data extraction, cleaning, analysis) to ensure API responsiveness.
    *   **Conceptual Worker Types:** Extraction Worker, Cleaning Worker, Analysis Worker.

5.  **AI Agents (Logical Components):**
    *   **a. Data Extractor Agent:** Extracts text, tables, and key-value pairs from various file formats using LLMs, OCR, and parsing libraries.
    *   **b. Data Cleaner Agent:** Cleans and normalizes raw extracted data.
    *   **c. Data Analyzer Agent:** Derives insights, generates summaries, and performs statistical analysis on cleaned data.

6.  **Data Stores:**
    *   **a. Object Storage (MinIO/S3):** Stores raw uploaded files, intermediate processed files, and large result files.
    *   **b. Relational Database (PostgreSQL):** Stores metadata (users, files, jobs), structured extracted data, and configurations.
    *   **c. Message Broker (RabbitMQ/Redis):** Manages the task queue for Celery workers.
    *   **d. Vector Database (Pinecone/Weaviate - Stretch Goal):** Stores vector embeddings for semantic search.

7.  **External Services / APIs:**
    *   **LLM APIs:** OpenAI, Anthropic, Google Gemini, etc.
    *   **Cloud-based OCR/AI Services (Optional):** Google Cloud Vision AI, AWS Textract.

### 2.2. High-Level Data Flow and Workflow

The data processing workflow is as follows:

1.  **File Upload:** User uploads a file via the Frontend. The API Gateway routes it to the File Ingestion Service, which stores the file in Object Storage and creates a job in PostgreSQL, notifying the Job Management Service.
2.  **Job Processing Initiation:** The Job Management Service places a task on the Message Broker.
3.  **Asynchronous Task Execution:** A Celery Worker picks up the task. Coordinated by the AI Orchestration Service, it executes the agent pipeline:
    *   **Data Retrieval:** Fetches the file from Object Storage.
    *   **Extraction Phase (Data Extractor Agent):** Performs OCR (if needed), parses the file, and extracts raw data.
    *   **Cleaning Phase (Data Cleaner Agent):** Normalizes the extracted data.
    *   **Analysis Phase (Data Analyzer Agent):** Generates summaries, statistics, and insights.
4.  **Storing Results:** The worker stores final results in PostgreSQL and/or Object Storage, updating the job status.
5.  **Displaying Results:** The Frontend polls for job completion and then requests results from the Results Service to display to the user.

### 2.3. Scalability and Modularity Considerations

*   **Microservices:** Independent scaling of backend services.
*   **Asynchronous Processing:** Decouples long tasks, maintaining API responsiveness.
*   **Stateless Services:** Facilitates scaling and load balancing.
*   **Database Scaling:** PostgreSQL supports read replicas/sharding. Object storage is inherently scalable.
*   **Containerization & Orchestration (Docker, Kubernetes):** Simplifies deployment, management, and auto-scaling.

## 3. AI Agent Architecture

The AI agents are logical components orchestrated by the AI Orchestration Service and executed by Celery workers. They leverage LLMs, specialized libraries, and custom logic.

### 3.1. AI Agent Roles

1.  **Data Extractor Agent:**
    *   **Responsibility:** Ingests raw files, performs OCR if needed, and extracts text, tables, and key-value pairs using LLMs and parsing tools.
    *   **Output:** Structured JSON with raw extracted data.

2.  **Data Cleaner Agent:**
    *   **Responsibility:** Cleans and normalizes the raw extracted data (whitespace, dates, numerics).
    *   **Output:** Structured JSON with cleaned, normalized data.

3.  **Data Analyzer Agent:**
    *   **Responsibility:** Processes cleaned data to derive insights, generate summaries, perform statistical analysis, and prepare data for visualization.
    *   **Output:** JSON object with analysis results (summaries, keywords, stats, visualization data).

### 3.2. Logic Chaining and Orchestration

The agents operate in a sequential pipeline:
1.  **Initiation:** Job creation passes the raw file to the Data Extractor Agent.
2.  **Extraction:** Output is passed to the Data Cleaner Agent.
3.  **Cleaning:** Output is passed to the Data Analyzer Agent.
4.  **Analysis:** Final results are compiled and stored.
Frameworks like LangChain or LlamaIndex manage LLM prompts, tool chaining, and context within and between agent operations.

## 4. Technology Stack and Key Integrations

The system leverages a carefully selected technology stack to achieve its goals. Refer to the "Proposed Technology Stack" and "Key APIs, Tools, and Libraries" sections in the main Technical System Design document for detailed justifications of each choice. Key elements include:

*   **Frontend:** Lovable.dev, potentially with Zustand/Redux Toolkit, Tailwind CSS, and Chart.js/Recharts/Nivo.
*   **Backend:** Python, FastAPI, Celery with RabbitMQ/Redis, PostgreSQL, MinIO/S3.
*   **AI/Data Processing:** OpenAI API (or alternatives), LangChain/LlamaIndex, Tesseract OCR (or cloud OCR), PyMuPDF, Pandas, python-docx, Camelot/Tabula-py, NLTK/spaCy.
*   **DevOps:** Docker, Kubernetes (stretch), GitHub Actions, Prometheus/Grafana/ELK (stretch).

These components interact as described in the data flow, with the API Gateway managing frontend-backend communication, backend services coordinating via the message broker and database, and AI agents utilizing various libraries and external APIs to process data.

This architectural design provides a resilient and adaptable foundation for the Universal Data Extractor + Analyzer, ensuring it can meet current requirements and evolve to incorporate more advanced functionalities in the future.
