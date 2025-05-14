# Technical System Design

## 1. Proposed Technology Stack

Choosing a modern, scalable, and robust technology stack is crucial for the success of the Universal Data Extractor + Analyzer. The proposed stack prioritizes developer productivity, performance, community support, and future-proofing.

### Frontend

*   **Framework/Platform:** **Lovable.dev** (as specified by the user)
    *   **Justification:** Lovable.dev is designated for UI development. We will leverage its capabilities for building a user-friendly and responsive interface. The focus will be on creating reusable components and a clear layout that aligns with the UI/UX flow to be defined later.
*   **State Management:** Depending on Lovable.dev's built-in capabilities, or a library like ** Zustand or Redux Toolkit** if external state management is needed and compatible.
    *   **Justification:** For managing complex application states, especially as features grow. Zustand is lightweight, and Redux Toolkit offers a structured approach.
*   **Styling:** **Tailwind CSS** or styled-components (if compatible and preferred within Lovable.dev environment).
    *   **Justification:** Tailwind CSS provides utility classes for rapid UI development and consistent styling. Styled-components offer component-level styling if a more encapsulated approach is desired.
*   **Charting/Visualization:** A library compatible with Lovable.dev, such as **Chart.js, Recharts, or Nivo**.
    *   **Justification:** These libraries offer a wide range of chart types and customization options for presenting analytical insights effectively.

### Backend

*   **Programming Language:** **Python**
    *   **Justification:** Python is the de facto language for AI/ML and data processing, with extensive libraries (Pandas, NumPy, Scikit-learn, spaCy, NLTK), robust frameworks, and a large community. Its readability and ease of integration make it ideal for this project.
*   **Framework:** **FastAPI**
    *   **Justification:** FastAPI is a modern, high-performance web framework for building APIs with Python 3.7+ based on standard Python type hints. It offers automatic data validation, serialization, interactive API documentation (Swagger UI, ReDoc), and asynchronous capabilities (ASGI), making it excellent for building scalable and maintainable backend services.
*   **Asynchronous Task Queue:** **Celery with RabbitMQ or Redis as a message broker**
    *   **Justification:** Data extraction and analysis can be time-consuming. Celery allows for offloading these tasks to background workers, preventing API timeouts and improving responsiveness. RabbitMQ is a robust message broker, while Redis can serve as a simpler alternative for smaller setups.
*   **Database (Primary):** **PostgreSQL**
    *   **Justification:** A powerful, open-source object-relational database system with a strong reputation for reliability, feature robustness, and performance. It can handle structured data (user accounts, job metadata, processed results) and has good support for JSONB for semi-structured data.
*   **Database (Vector/Search - for Stretch Goals):** **Pinecone, Weaviate, or Elasticsearch with vector search capabilities**
    *   **Justification:** For advanced features like semantic search on extracted text or finding similar documents, a dedicated vector database or a search engine with vector support will be essential for efficient similarity searches.
*   **Object Storage:** **MinIO or AWS S3 (or compatible)**
    *   **Justification:** For storing uploaded user files, intermediate processing files, and potentially large output files. Object storage is scalable, cost-effective, and durable.

### AI / Data Processing

*   **LLM Integration:**
    *   **Primary Choice:** **OpenAI API (GPT-4, GPT-3.5-turbo)** or other leading foundation models (e.g., Anthropic Claude, Google Gemini) via their respective APIs.
    *   **Justification:** State-of-the-art capabilities in natural language understanding, generation, text extraction, summarization, and function calling. API access simplifies integration and avoids the need for self-hosting large models initially.
    *   **Framework for LLM Interaction:** **LangChain or LlamaIndex**
        *   **Justification:** These frameworks simplify building applications with LLMs by providing tools for prompt management, agent creation, chaining, data integration, and interaction with external tools/APIs.
*   **OCR (Optical Character Recognition):**
    *   **Primary Choice:** **Tesseract OCR** (open source)
    *   **Cloud-based alternatives (for higher accuracy/more features):** Google Cloud Vision AI, AWS Textract.
    *   **Justification:** Tesseract is a capable open-source OCR engine. Cloud services can offer superior accuracy, broader language support, and specialized features like form and table extraction from images, especially for the MVP and beyond.
*   **PDF Processing:**
    *   **Python Libraries:** **PyMuPDF (fitz), pdfminer.six, pypdfium2** for text and basic layout extraction.
    *   **Camelot or Tabula-py** for table extraction from PDFs.
    *   **Justification:** These libraries provide robust tools for parsing PDF content, extracting text, images, and identifying tabular structures.
*   **Spreadsheet Processing:**
    *   **Python Library:** **Pandas** (for .csv, .xlsx, .xls)
    *   **Justification:** Pandas is the standard Python library for data manipulation and analysis, offering excellent support for reading and writing various spreadsheet formats.
*   **Document Processing (e.g., .docx):**
    *   **Python Library:** **python-docx**
    *   **Justification:** Allows reading and extracting content from Microsoft Word documents.
*   **Data Manipulation and Analysis:**
    *   **Python Libraries:** **Pandas, NumPy, Scikit-learn, spaCy, NLTK**
    *   **Justification:** Core libraries for data cleaning, transformation, statistical analysis, natural language processing (NLP) tasks like keyword extraction, and potentially sentiment analysis or topic modeling in later stages.

### DevOps and Infrastructure

*   **Containerization:** **Docker**
    *   **Justification:** Ensures consistent environments across development, testing, and production. Simplifies deployment and scaling.
*   **Orchestration (for scaling):** **Kubernetes (K8s)** or a simpler PaaS solution (e.g., Docker Swarm, AWS ECS, Google Cloud Run) depending on initial scale and complexity.
    *   **Justification:** Kubernetes provides robust orchestration for managing containerized applications, enabling auto-scaling, self-healing, and efficient resource utilization. PaaS options can offer a lower operational overhead for initial deployment.
*   **CI/CD:** **GitHub Actions**
    *   **Justification:** Integrated with the GitHub repository for automated testing, building, and deployment pipelines.
*   **Monitoring and Logging:** **Prometheus, Grafana, ELK Stack (Elasticsearch, Logstash, Kibana) or cloud-native solutions (e.g., AWS CloudWatch, Google Cloud Monitoring).**
    *   **Justification:** Essential for observing system health, performance, and troubleshooting issues in a production environment.

This technology stack provides a flexible and powerful foundation for building the Universal Data Extractor + Analyzer, capable of supporting the MVP features and scaling to accommodate future stretch goals.



## 2. Overall Architecture, Components, and Data Flow

The Universal Data Extractor + Analyzer will be designed as a modular, microservices-oriented architecture to ensure scalability, maintainability, and flexibility. This approach allows individual components to be developed, deployed, and scaled independently.

### Core System Components

1.  **Frontend (Client Application):**
    *   **Description:** The user-facing interface, built with Lovable.dev. It will be responsible for handling user interactions, file uploads, displaying extracted data and analysis results, and rendering visualizations.
    *   **Key Functions:** User authentication (stretch goal), file selection and upload, job status monitoring, results display (text, tables, charts), user input for analysis parameters (stretch goal).

2.  **API Gateway:**
    *   **Description:** A single entry point for all client requests. It routes requests to the appropriate backend services, handles authentication and authorization (stretch goal), rate limiting, and request/response transformations.
    *   **Technology:** Can be built using FastAPI itself or a dedicated gateway solution like Kong, Tyk, or cloud provider gateways (e.g., AWS API Gateway, Google Cloud API Gateway).

3.  **Backend Services (FastAPI):**
    *   **a. File Ingestion Service:**
        *   **Description:** Handles incoming file uploads from the frontend. Responsible for validating file types and sizes, and securely storing the raw uploaded files in Object Storage (e.g., MinIO/S3).
        *   **Key Functions:** Receive file streams, validate metadata, store files, create initial job records in the database.
    *   **b. Job Management Service:**
        *   **Description:** Manages the lifecycle of data extraction and analysis jobs. It creates tasks for the asynchronous task queue (Celery) and updates job statuses in the PostgreSQL database.
        *   **Key Functions:** Create new jobs, dispatch tasks to workers, track job progress (e.g., pending, processing, completed, failed), retrieve job results.
    *   **c. AI Orchestration Service (Agent Controller):**
        *   **Description:** The core logic unit that coordinates the sequence of AI agent operations (Extractor, Cleaner, Analyzer). It fetches data, calls the appropriate LLMs or specialized tools/libraries, and manages the flow of data between agents.
        *   **Key Functions:** Implement agent chaining logic, interact with LLM APIs (OpenAI, etc.) via LangChain/LlamaIndex, call specialized libraries for OCR, PDF parsing, etc., manage intermediate data states.
    *   **d. Results Service:**
        *   **Description:** Provides processed and analyzed data to the frontend. Fetches results from the database or object storage (for larger outputs) and formats them for display.
        *   **Key Functions:** Retrieve structured data, summaries, analytical insights, and visualization data; format for API responses.

4.  **Asynchronous Task Workers (Celery):**
    *   **Description:** A pool of background workers that execute long-running tasks such as file parsing, OCR, data extraction, cleaning, and analysis. This ensures the API remains responsive.
    *   **Key Functions:** Consume tasks from the message broker (RabbitMQ/Redis), execute the core processing logic by invoking AI agents and data processing libraries, update job status, and store results.
    *   **Individual Worker Types (Conceptual):**
        *   **Extraction Worker:** Handles file-specific parsing (PDF, DOCX, CSV, image OCR) and initial data extraction using LLMs or rule-based methods.
        *   **Cleaning Worker:** Performs data normalization, type conversion, and quality checks.
        *   **Analysis Worker:** Executes analytical tasks, generates summaries, performs statistical calculations, and creates data for visualizations.

5.  **AI Agents (Logical Components, implemented within workers/orchestration service):**
    *   **a. Data Extractor Agent:**
        *   **Description:** Responsible for identifying and extracting relevant information (text, tables, key-value pairs) from various file formats. Utilizes LLMs, OCR tools, and parsing libraries.
    *   **b. Data Cleaner Agent:**
        *   **Description:** Takes the raw extracted data and performs cleaning and normalization operations (e.g., whitespace trimming, date standardization, numeric cleaning).
    *   **c. Data Analyzer Agent:**
        *   **Description:** Processes the cleaned, structured data to derive insights, generate summaries, perform statistical analysis, and identify trends or anomalies.

6.  **Data Stores:**
    *   **a. Object Storage (MinIO/S3):**
        *   **Description:** Stores raw uploaded files, intermediate processed files (e.g., OCR output), and potentially large result files (e.g., extensive reports, large CSV exports).
    *   **b. Relational Database (PostgreSQL):**
        *   **Description:** Stores metadata about users (stretch goal), uploaded files, job status, job history, extracted structured data (if not too large, or pointers to object storage), and configuration settings.
    *   **c. Message Broker (RabbitMQ/Redis):**
        *   **Description:** Facilitates communication between the API services and the Celery workers, managing the task queue.
    *   **d. Vector Database (Pinecone/Weaviate - Stretch Goal):**
        *   **Description:** Stores vector embeddings of textual content for semantic search and similarity analysis.

7.  **External Services / APIs:**
    *   **LLM APIs:** OpenAI, Anthropic, Google Gemini, etc.
    *   **Cloud-based OCR/AI Services (Optional):** Google Cloud Vision AI, AWS Textract for enhanced extraction capabilities.

### High-Level Data Flow and Workflow

1.  **File Upload:**
    *   The user selects a file via the **Frontend** (Lovable.dev interface).
    *   The Frontend sends the file to the **API Gateway**, which routes it to the **File Ingestion Service**.
    *   The File Ingestion Service validates the file, stores it in **Object Storage**, and creates an initial job record in the **PostgreSQL Database** with a "pending" status. It then notifies the **Job Management Service**.

2.  **Job Processing Initiation:**
    *   The **Job Management Service** receives the new job notification.
    *   It creates a task (e.g., "process_file") and places it onto the **Message Broker** (RabbitMQ/Redis).
    *   The Job Management Service updates the job status in PostgreSQL to "queued".

3.  **Asynchronous Task Execution (Celery Workers):**
    *   An available **Celery Worker** picks up the task from the Message Broker.
    *   The worker, coordinated by the **AI Orchestration Service** logic, begins the processing pipeline:
        *   **a. Data Retrieval:** The worker fetches the raw file from Object Storage based on the job details.
        *   **b. Extraction Phase (Data Extractor Agent):**
            *   If the file is an image or a non-searchable PDF, OCR (Tesseract or cloud service) is performed.
            *   Relevant parsing libraries (PyMuPDF, Pandas, python-docx) are used based on file type.
            *   The **Data Extractor Agent** (leveraging LLMs via LangChain/LlamaIndex and specialized tools) extracts text, tables, and key-value pairs.
            *   Intermediate extracted data might be temporarily stored or passed in memory.
        *   **c. Cleaning Phase (Data Cleaner Agent):**
            *   The raw extracted data is passed to the **Data Cleaner Agent**.
            *   It applies normalization rules (whitespace, date formats, numeric cleaning).
        *   **d. Analysis Phase (Data Analyzer Agent):**
            *   The cleaned, structured data is passed to the **Data Analyzer Agent**.
            *   It performs summarization, statistical analysis, keyword extraction, and prepares data for visualizations.

4.  **Storing Results:**
    *   The Celery worker, upon completion of all phases, stores the final structured data, summaries, and analysis results in the **PostgreSQL Database**. Large outputs (e.g., full extracted text if very long, or generated reports) might be stored in **Object Storage**, with a reference in PostgreSQL.
    *   The worker updates the job status in PostgreSQL to "completed" (or "failed" if errors occurred, along with error details).

5.  **Displaying Results:**
    *   The **Frontend** periodically polls the **Job Management Service** (or uses WebSockets for real-time updates - a stretch goal) for the job status.
    *   Once the job is marked "completed", the Frontend requests the results from the **Results Service** (via the API Gateway).
    *   The Results Service fetches the processed data from PostgreSQL (and/or Object Storage) and sends it back to the Frontend.
    *   The Frontend displays the extracted information, tables, summaries, and visualizations (charts) to the user.
    *   The user has options to view different aspects of the results and download extracted data (e.g., as CSV).

### Scalability and Modularity Considerations

*   **Microservices:** Each backend service (File Ingestion, Job Management, AI Orchestration, Results) can be scaled independently based on load. For example, if data extraction is the bottleneck, more Celery workers and AI Orchestration service instances can be deployed.
*   **Asynchronous Processing:** The use of Celery and a message broker decouples long-running tasks from the synchronous API requests, allowing the system to handle many concurrent users and large files without degrading frontend responsiveness.
*   **Stateless Services:** Backend services should be designed to be stateless where possible, allowing for easier scaling and load balancing.
*   **Database Scaling:** PostgreSQL can be scaled using read replicas or sharding for very high loads. Object storage is inherently scalable.
*   **Containerization (Docker) and Orchestration (Kubernetes):** Simplify deployment, management, and auto-scaling of services.

This architecture provides a robust foundation for the Universal Data Extractor + Analyzer, supporting the MVP features while being extensible for the planned stretch goals, such as incorporating more advanced AI capabilities, wider file type support, and enhanced user interaction features.



## 3. AI Agent Roles and Logic Chaining

The Universal Data Extractor + Analyzer relies on a coordinated sequence of AI-powered agents to process data from raw files to actionable insights. These agents are logical constructs, implemented within the AI Orchestration Service and executed by Celery workers. They leverage a combination of Large Language Models (LLMs) through frameworks like LangChain or LlamaIndex, specialized data processing libraries, and custom logic.

### AI Agent Roles

1.  **Data Extractor Agent:**
    *   **Primary Responsibility:** To ingest raw files of various formats and accurately extract all relevant content, including text, tables, and key-value pairs, transforming unstructured or semi-structured data into a structured machine-readable format.
    *   **Inputs:** Raw file (PDF, TXT, CSV for MVP; DOCX, images with OCR, web page URLs for stretch goals).
    *   **Key Operations:**
        *   **File Type Identification:** Determine the type of input file to apply appropriate parsing strategies.
        *   **OCR (Optical Character Recognition):** For image-based files (scanned PDFs, JPG, PNG, TIFF - stretch goal), convert images of text into machine-readable text using Tesseract or cloud-based OCR services.
        *   **Content Parsing:** Utilize specialized libraries (e.g., PyMuPDF for PDFs, Pandas for CSVs, python-docx for DOCX) to access the file's internal structure and content streams.
        *   **Text Extraction:** Extract all discernible textual content, maintaining a logical reading order where possible. For complex layouts, LLMs can assist in segmenting and ordering text blocks.
        *   **Table Extraction:** Identify and extract tabular data. This can range from simple CSV parsing to complex table recognition in PDFs or images using libraries like Camelot/Tabula-py or LLM-driven visual document understanding techniques.
        *   **Key-Value Pair Extraction:** Identify and extract specific data points presented as key-value pairs (e.g., "Invoice Number: INV-123", "Date: 2023-10-26"). This is heavily reliant on LLM prompts for MVP, especially for diverse document types. For stretch goals, this can be enhanced with user-defined schemas or template-based extraction.
    *   **Tools & Techniques:** LLMs (OpenAI API via LangChain/LlamaIndex), Tesseract OCR, PyMuPDF, Pandas, python-docx, Camelot, Tabula-py.
    *   **Output:** A structured JSON object containing the extracted raw data. This might include arrays of text blocks, lists of tables (where each table is a list of rows, and each row is a list of cell contents), and a dictionary of identified key-value pairs. Example: `{"text_content": "...", "tables": [{"name": "table1", "data": [["col1", "col2"], ["val1", "val2"]]}], "key_fields": {"InvoiceID": "123", "Date": "2024-05-14"}}`.

2.  **Data Cleaner Agent:**
    *   **Primary Responsibility:** To take the raw extracted data from the Extractor Agent and perform various cleaning and normalization operations to improve data quality, consistency, and suitability for analysis.
    *   **Inputs:** The structured JSON output from the Data Extractor Agent.
    *   **Key Operations:**
        *   **Whitespace Management:** Trim leading/trailing whitespace from all textual data elements.
        *   **Case Normalization (Optional):** Convert text to a consistent case (e.g., lowercase) if appropriate for the specific data field and downstream analysis.
        *   **Date Standardization:** Identify various date formats and convert them to a standard ISO 8601 format (YYYY-MM-DD or YYYY-MM-DDTHH:MM:SSZ).
        *   **Numeric Value Cleaning:** Remove currency symbols (e.g., $, €), commas as thousand separators, and other non-numeric characters from potential numeric fields, then convert to standard numeric types (integer, float).
        *   **Special Character Handling:** Sanitize or escape special characters that might interfere with further processing or database storage.
        *   **Data Type Inference and Correction (Stretch Goal):** Attempt to infer the correct data type for each field (string, number, boolean, date) and perform necessary conversions.
        *   **Handling Missing or Null Values (Basic):** Ensure consistent representation of missing values (e.g., `null` or empty string based on policy).
        *   **Redundancy Removal (Basic):** Remove duplicate entries if applicable (e.g., repeated headers in tables extracted across pages).
    *   **Tools & Techniques:** Python string manipulation, regular expressions, dateutil library, Pandas (if data is temporarily loaded into DataFrames for cleaning), LLMs for more complex contextual cleaning (stretch goal, e.g., resolving ambiguous abbreviations).
    *   **Output:** A structured JSON object, mirroring the input format, but with the data values cleaned and normalized.

3.  **Data Analyzer Agent:**
    *   **Primary Responsibility:** To process the cleaned, structured data to derive meaningful insights, generate summaries, perform statistical calculations, identify patterns or anomalies, and prepare data for visualization.
    *   **Inputs:** The cleaned and structured JSON output from the Data Cleaner Agent.
    *   **Key Operations (MVP focus on basic analysis):**
        *   **Text Analysis:**
            *   **Summarization:** Generate concise summaries of large blocks of extracted text using LLMs (abstractive or extractive).
            *   **Keyword Extraction:** Identify and list the most frequent or contextually relevant keywords/phrases (e.g., using TF-IDF, RAKE, or LLM-based methods).
        *   **Tabular Data Analysis:**
            *   **Descriptive Statistics:** For numeric columns in extracted tables, calculate count, sum, mean, median, minimum, maximum, and standard deviation.
            *   **Frequency Distributions:** For categorical columns, calculate the frequency of each unique value.
        *   **Key-Value Data Analysis:** Present the cleaned key-value pairs as a structured summary. Highlight any missing predefined essential keys (stretch goal).
        *   **Insight Generation (Basic):** Based on the analysis, generate simple textual insights (e.g., "The average transaction value is X", "The most common keyword is Y").
        *   **Data Preparation for Visualization:** Transform analyzed data into formats suitable for charting libraries (e.g., data series for bar charts, pie charts).
    *   **Stretch Goal Operations:** Sentiment analysis, topic modeling, trend analysis, anomaly detection, comparative analysis across multiple documents, natural language querying of the data.
    *   **Tools & Techniques:** LLMs (OpenAI API via LangChain/LlamaIndex for summarization, insight generation), Pandas and NumPy for statistical calculations, NLTK/spaCy for NLP tasks (keyword extraction, potentially sentiment analysis), Scikit-learn for more advanced analytics.
    *   **Output:** A JSON object containing the analysis results. This would include sections for summaries, keyword lists, statistical tables, textual insights, and data series formatted for frontend charting. Example: `{"summary": "...", "keywords": ["a", "b"], "table_analysis": {"table1_stats": {...}}, "visualizations": {"chart1_data": {...}}}`.

### Logic Chaining and Orchestration

The AI agents operate in a sequential pipeline, orchestrated by the AI Orchestration Service, typically executed within Celery workers for asynchronous processing:

1.  **Initiation:** A new job is created upon file upload. The raw file is passed to the **Data Extractor Agent**.
2.  **Extraction:** The Data Extractor Agent processes the file, performs OCR if needed, and extracts raw text, tables, and key-value pairs. Its structured output is then passed to the next agent.
3.  **Cleaning:** The **Data Cleaner Agent** receives the raw extracted data. It applies a series of normalization and cleaning rules to each relevant data element.
The cleaned, structured data is then passed forward.
4.  **Analysis:** The **Data Analyzer Agent** receives the cleaned data. It performs various analytical tasks based on the data's nature (textual, tabular) and configured analysis types. It generates summaries, statistical insights, and data for visualizations.
5.  **Result Aggregation:** The outputs from the Analyzer Agent (and potentially intermediate outputs from other agents if needed for display, like raw extracted text) are compiled and stored (e.g., in PostgreSQL or Object Storage) to be made available to the user via the frontend.

This chained approach ensures that data flows logically through stages of refinement and analysis, with each agent specializing in its designated role. The use of LangChain/LlamaIndex will be pivotal in managing prompts for LLMs, chaining LLM calls with other tools (like code execution or API calls to specialized libraries), and maintaining context across different steps within an agent's operation or even between agents if a more complex interaction model is adopted in later stages.



## 4. Key APIs, Tools, and Libraries

This section details the specific APIs, software tools, and programming libraries that will be integral to the development and operation of the Universal Data Extractor + Analyzer. These choices align with the proposed technology stack and are crucial for implementing the system's features, from MVP to stretch goals.

### External APIs

1.  **Large Language Model (LLM) APIs:**
    *   **Primary:** **OpenAI API** (Models: GPT-4, GPT-3.5-turbo, and potentially future models for text generation, summarization, key-value extraction, question answering, and function calling).
        *   **Usage:** Core of the AI agents for understanding document content, extracting structured information from unstructured text, cleaning data contextually, and generating analytical insights and summaries.
    *   **Alternatives (for flexibility or specific needs - Stretch Goal):**
        *   **Anthropic Claude API:** For strong conversational and text processing capabilities.
        *   **Google Gemini API:** For multimodal understanding and generation.
    *   **Access:** Via official Python client libraries (e.g., `openai`).

2.  **Cloud-based OCR and Document AI Services (Optional, for enhanced accuracy/features - Stretch Goal):**
    *   **Google Cloud Vision AI API:** For advanced OCR, handwriting recognition, document text detection, and entity recognition from images and PDFs.
    *   **AWS Textract:** Specialized for extracting text, handwriting, and data from scanned documents, forms, and tables.
    *   **Microsoft Azure AI Document Intelligence (formerly Form Recognizer):** For extracting text, key-value pairs, tables, and structures from documents.
    *   **Usage:** To supplement or replace local OCR (Tesseract) when higher accuracy, broader language support, or specialized document understanding features (e.g., pre-trained models for invoices, receipts) are required.
    *   **Access:** Via official Python SDKs provided by Google Cloud, AWS, and Azure.

### Core Backend Tools and Libraries (Python)

1.  **Web Framework & API Development:**
    *   **FastAPI:** For building efficient, modern RESTful APIs.
    *   **Uvicorn:** ASGI server to run FastAPI applications.
    *   **Pydantic:** For data validation and settings management (used intrinsically by FastAPI).

2.  **Asynchronous Task Processing:**
    *   **Celery:** Distributed task queue for handling background processing of extraction, cleaning, and analysis jobs.
    *   **RabbitMQ (Message Broker):** Robust message broker for Celery (recommended for production).
    *   **Redis (Message Broker/Cache):** Alternative message broker for Celery, also useful for caching.

3.  **Database Interaction:**
    *   **SQLAlchemy:** ORM (Object Relational Mapper) for interacting with PostgreSQL, providing an abstraction layer over SQL.
    *   **psycopg2-binary or asyncpg:** PostgreSQL adapter for Python (asyncpg for FastAPI's asynchronous operations).
    *   **MinIO Client (mc or Python library `minio`):** For interacting with MinIO object storage.
    *   **Boto3 (if using AWS S3):** AWS SDK for Python, for S3 interaction.

4.  **LLM Orchestration & Interaction:**
    *   **LangChain:** Framework for developing applications powered by language models. Used for prompt engineering, agent creation, chaining LLM calls with other tools, and managing context.
    *   **LlamaIndex:** Data framework for LLM applications, focusing on connecting LLMs with external data sources (ingestion, indexing, querying).

5.  **File Parsing and Extraction:**
    *   **PyMuPDF (fitz):** For PDF parsing, text extraction, image extraction, and accessing metadata from PDF files. Known for its speed and comprehensive features.
    *   **pdfminer.six:** Alternative library for PDF text extraction and analysis.
    *   **pypdfium2:** Python bindings to PDFium, a Google-developed PDF rendering engine, useful for robust PDF processing.
    *   **Pandas:** For reading, writing, and manipulating data from CSV, Excel (.xlsx, .xls) files. Also used for data structuring and analysis.
    *   **python-docx:** For extracting text and structure from Microsoft Word (.docx) files.
    *   **Pillow (PIL Fork):** For image manipulation tasks if needed before OCR (e.g., preprocessing).
    *   **OpenCV (cv2):** For advanced image processing tasks, potentially for layout analysis or table detection in images before OCR (Stretch Goal).

6.  **OCR Engine:**
    *   **Tesseract OCR (via `pytesseract` Python wrapper):** Open-source OCR engine for converting images of text into machine-readable text. MVP will rely on this for basic image-to-text.

7.  **Table Extraction (from PDFs/Images):**
    *   **Camelot-py:** Python library specifically for extracting tables from PDF files. Relies on Ghostscript.
    *   **Tabula-py:** Python wrapper for Tabula, another tool for extracting tables from PDFs.
    *   (LLM-based visual document understanding will also be explored for table extraction, especially for complex or image-based tables).

8.  **Data Cleaning and Normalization:**
    *   **Standard Python Libraries:** `re` (regular expressions), `datetime`, `string` modules.
    *   **dateutil (python-dateutil):** For robust parsing of various date string formats.
    *   **NumPy:** For numerical operations and data type conversions, often used in conjunction with Pandas.

9.  **Data Analysis and NLP:**
    *   **Pandas:** Core library for data manipulation, aggregation, and analysis of structured (tabular) data.
    *   **NumPy:** Fundamental package for numerical computation in Python.
    *   **Scikit-learn:** For machine learning tasks, including potential use in classification, clustering, outlier detection, or more advanced NLP features (TF-IDF, etc.) (Stretch Goal).
    *   **NLTK (Natural Language Toolkit):** For basic NLP tasks like tokenization, stemming, part-of-speech tagging, and keyword extraction (e.g., RAKE algorithm).
    *   **spaCy:** For more advanced and efficient NLP tasks, including named entity recognition (NER), dependency parsing, and pre-trained word vectors (Stretch Goal).

### Frontend Tools and Libraries (Lovable.dev Environment)

1.  **Core Platform:**
    *   **Lovable.dev:** The primary platform for UI development, component building, and user interaction logic, as specified.

2.  **State Management (if needed beyond Lovable.dev built-ins):**
    *   **Zustand or Redux Toolkit:** For managing global application state if Lovable.dev's native capabilities are insufficient for the complexity.

3.  **Styling:**
    *   **Tailwind CSS (preferred):** Utility-first CSS framework for rapid UI development.
    *   **Styled-components or Emotion:** If a CSS-in-JS approach is more suitable within Lovable.dev.

4.  **Charting and Visualization:**
    *   **Chart.js:** Simple yet flexible JavaScript charting library.
    *   **Recharts:** A composable charting library built on React components (if Lovable.dev supports React-like component models).
    *   **Nivo:** Provides a rich set of server-side rendered charts and data visualization components, often React-based.
    *   (The choice will depend on ease of integration with Lovable.dev and the specific visualization needs).

5.  **API Communication:**
    *   **Fetch API (native browser API) or Axios:** For making HTTP requests from the frontend to the backend API Gateway.

### DevOps and Infrastructure Tools

1.  **Containerization:**
    *   **Docker & Docker Compose:** For creating consistent development and deployment environments, and for local orchestration.

2.  **Orchestration (Stretch Goal for Production Scaling):**
    *   **Kubernetes:** For managing containerized applications at scale.
    *   **Helm:** Package manager for Kubernetes.

3.  **CI/CD:**
    *   **GitHub Actions:** For automating build, test, and deployment pipelines integrated with the project repository.

4.  **Monitoring and Logging (Stretch Goal for Production):**
    *   **Prometheus:** Monitoring system and time series database.
    *   **Grafana:** Visualization dashboard for metrics from Prometheus.
    *   **ELK Stack (Elasticsearch, Logstash, Kibana):** For centralized logging and log analysis.

This list provides a comprehensive overview of the key technological components. The selection prioritizes open-source, well-supported, and production-ready options that align with the project's goals of scalability, modularity, and leveraging cutting-edge AI capabilities.
