# Portfolio Projects

Welcome to my project portfolio. This repository showcases a curated set of technical projects demonstrating applied skills in automation, real-time audio processing, retrieval-augmented generation (RAG), and data science. These projects highlight my capabilities with Python, LLM tools, browser automation, and cloud-ready backend development.

---

## Projects

### 1. Real-Time Audio Transcriber Backend
A modular backend service for capturing, chunking, and transcribing audio from both microphone and system sources in real-time. It uses Silero VAD for segmentation and FasterWhisper for transcription, outputting structured data suitable for downstream LLM pipelines.

**Key Features:**
- Dual-source capture (mic + system audio)
- Real-time VAD-based segmentation
- Optional background transcription
- JSON output format
- Designed for integration with RAG systems like PipeCat or Ollama

**Tech Stack:** Python, Silero VAD, FasterWhisper, SoundDevice, SciPy

**Use Cases:** Meeting summarization, real-time Q&A input, LLM-driven assistants

---

### 2. QA Form Filler
A browser automation tool designed for QA professionals and developers to automate and test web form behavior. Supports both Playwright and Selenium with realistic data generation via Faker.

**Key Features:**
- Cross-browser support (Playwright and Selenium)
- Field interaction (text, dropdowns, checkboxes, etc.)
- Screenshot and CSV logging
- CLI with headless and submission options

**Tech Stack:** Python, Playwright, Selenium, Faker, CSV logging

**Use Cases:** Automated form validation, QA pipelines, website regression testing

---

### 3. LangChain RAG Assistant
A RAG pipeline combining LangChain, Ollama, and ChromaDB, enabling PDF document ingestion, semantic indexing, and interactive querying through a Streamlit UI. Supports containerized workspaces for document organization.

**Key Features:**
- PDF ingestion and parsing
- Text chunking + embedding with Ollama
- ChromaDB vector search
- Streamlit UI for LLM Q&A
- Source-backed citations in responses

**Tech Stack:** Python, LangChain, Ollama, ChromaDB, Streamlit, PyMuPDF

**Use Cases:** Context-aware document Q&A, knowledge management tools

---

### 4. IBM Data Science Projects
Selected assignments and projects completed as part of the IBM Data Science Professional Certificate program. These highlight foundational skills in data wrangling, analysis, visualization, and basic ML workflows.

**Key Features:**
- Data cleaning and transformation
- Jupyter Notebook use
- Exploratory data analysis and visualization
- Model training and evaluation

**Tech Stack:** Python, Pandas, Matplotlib, Scikit-learn

---

## Future Directions

Additional projects are under consideration that will explore advanced tooling, cloud integration, and LLM-focused applications. These may include:

- **Automated Web Scraping Pipeline** — A cloud-deployable solution using Playwright and AWS Lambda to periodically scrape and structure content for knowledge graphs and RAG indexing.
- **Data Dashboarding Toolkit** — An interactive data dashboard using Plotly Dash or Streamlit to visualize insights from dynamic or user-uploaded datasets.
- **LLM Plugin Prototypes** — Custom plugins for OpenAI or Ollama models to extend chatbot capabilities with web search, database querying, or file handling.
- **Cloud-Native ML Workflow** — End-to-end machine learning workflow leveraging cloud storage, model deployment, and CI/CD with GitHub Actions.

These concepts are intended to expand the portfolio over time as interest and relevance align.

---

## Skills Highlighted

- **Languages:** Python 3.10+
- **Browser Automation:** Playwright, Selenium
- **LLM and NLP Tools:** Whisper, FasterWhisper, Silero VAD, LangChain, Ollama
- **Data Engineering:** ChromaDB, CSV, JSON, Embedding APIs
- **Frontend/UI:** Streamlit
- **Audio Processing:** SoundDevice, SciPy, ASIO Bridge (Windows)
- **Data Science:** Pandas, Scikit-learn, Matplotlib
- **Tooling:** Git, pytest, virtual environments, CLI utilities

---

## License

All projects are released under the [MIT License](./LICENSE) unless otherwise noted in individual project folders.

## Navigation

Click into each project directory above to view its standalone README, instructions, and usage examples.
