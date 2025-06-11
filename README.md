# Portfolio Projects

Welcome to my portfolio repository. This collection showcases a range of applied projects in data science, real-time audio processing, large language models (LLMs), and AI tooling. Each project demonstrates hands-on experience with technologies like Python, Playwright, Selenium, Whisper, RAG pipelines, and cloud-ready backends.

## Projects

### audio-transcriber-backend

A real-time backend that captures both microphone and system audio, detects speech using voice activity detection (VAD), and transcribes speech using FasterWhisper. Designed to serve as an input pipeline for LLMs or retrieval-augmented generation (RAG) tools like PipeCat or Ollama.

- Dual-source audio streaming (mic and system)
- Silero VAD and Whisper integration
- Outputs structured transcriptions per utterance
- Built for low-latency, modular use

### qa-form-filler

A Python-based automation tool for quality assurance professionals and developers who need to test form behavior on websites. Built using Playwright and optionally Selenium, this tool simulates realistic user input for text fields, selectors, radio buttons, checkboxes, and more.

- Playwright-based form automation with optional Selenium fallback
- Randomized form input using Faker
- Headless mode, screenshot capture, and structured CSV logging
- CLI options for submitting forms, switching engines, and login
- Designed for batch testing via a JSON URL list

Note: Some fields, such as complex date pickers and file upload selectors, may not be fully supported depending on implementation. These are noted in logs when encountered.

### Coming Soon

### rag-reader-system

A Python-based RAG system that processes and indexes local documents (ebooks, PDFs, notes) to enable natural language querying. Includes:

- Document ingestion and chunking
- Embedding and vector store indexing
- Conversational interface for real-time retrieval
- Backend integration with models like Ollama or OpenRouter

### ibm-data-science-projects

Selected projects and exercises from the IBM Data Science Professional Certificate program, demonstrating:

- Data cleaning, wrangling, and visualization
- Model training and evaluation
- Jupyter Notebooks and Python best practices
- Use of tools like Pandas, Matplotlib, and Scikit-learn

### More Projects to Come

Future additions may include:

- Data analysis dashboards
- Automated web scraping pipelines
- Custom LLM tools and plugins
- ML workflows using cloud-native infrastructure

## Skills Highlighted

- Python, Playwright, Selenium
- Faker, WebDriver Manager, CLI design
- Real-time audio processing (SoundDevice, ASIO Bridge)
- Whisper and Silero VAD integration
- LLM orchestration (RAG, Ollama, PipeCat)
- Data Science workflows (Pandas, Scikit-learn, Matplotlib)
- Git, testing, modular architecture

## License

All projects are released under the MIT license unless otherwise noted.

## Navigation

Click into each project directory above to view its standalone README, instructions, and usage examples.
