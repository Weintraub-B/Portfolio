# LangChain RAG Assistant

## Overview

This project implements a streamlined **Retrieval-Augmented Generation (RAG)** pipeline using **LangChain**, **Ollama**, and **ChromaDB**, allowing users to upload, index, and query PDF documents via a browser interface built with **Streamlit**.

It combines document parsing, chunking, embedding via Ollama models, and local vector database storage for real-time semantic search powered by LLMs like **Mistral**.

---

## Key Features

- **PDF Document Ingestion**  
  Automatically extracts text and images from uploaded PDF files using PyMuPDF.

- **Text Chunking and Embedding**  
  Utilizes RecursiveCharacterTextSplitter and Ollama's embedding API for semantic chunk embedding.

- **Local Vector Storage**  
  Stores embeddings using ChromaDB for high-speed similarity search.

- **Ollama-Powered LLM QA**  
  Uses ChatOllama and Mistral for intelligent responses with reference-backed answers.

- **Document-Aware QA**  
  Retrieves source context and page-level image metadata to support user queries with citations.

- **Multi-Container Workspace**  
  Users can organize documents into isolated containers for flexible experimentation.

---

## Project Structure

```
langchain_rag_portfolio/
├── app/
│   └── main.py                  # Streamlit UI and logic
├── raglib/
│   └── ingest.py                # PDF parsing and image handling
├── containers/                  # User-created data environments
│   └── <your_container>/
│       ├── data/                # PDF files
│       ├── chroma_index/        # Chroma vector index
│       └── ingested_files.json  # Tracking info
├── requirements.txt
├── README.md
└── .gitignore
```

---

## Setup Instructions

### Prerequisites

- Python 3.10 or higher
- Ollama installed and running locally (`ollama run mistral`)
- One or more PDF documents for testing

### Install Dependencies

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Launch Application

```bash
streamlit run app/main.py
```

---

## Usage Workflow

1. Start the Ollama server and ensure the Mistral model is available.
2. Create a new container via the sidebar in the app.
3. Upload your PDF files.
4. Click "Ingest" to extract, chunk, embed, and store document data.
5. Use the input field to ask questions. Results are contextually retrieved and referenced.

---

## Technologies Used

| Component         | Tool/Library                  |
|------------------|-------------------------------|
| LLM Inference     | Ollama with Mistral           |
| RAG Framework     | LangChain                     |
| Embeddings        | OllamaEmbeddings              |
| Vector Store      | Chroma                        |
| User Interface    | Streamlit                     |
| PDF Processing    | PyMuPDF (fitz)                |
| Image Processing  | PIL, OpenCV                   |

---

## Example Output

**User Query:**  
What are the nutritional benefits of oyster mushrooms?

**Answer:**  
Oyster mushrooms are rich in protein, B vitamins, and essential minerals such as iron and potassium. They have also shown potential for lowering cholesterol and improving immune response.

**Sources:**  
- mushrooms_nutrition.pdf, Page 23

---

## Limitations

- Currently limited to PDFs only.
- Accuracy depends on embedding quality and the LLM used.
- Ingestion time increases with larger document sets.

---

## License

This project is released under the MIT License.
---

## Acknowledgments

- LangChain
- Ollama
- ChromaDB
- PyMuPDF
- Streamlit
