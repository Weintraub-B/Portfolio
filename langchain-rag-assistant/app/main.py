import os
import sys
import json
from pathlib import Path
from datetime import datetime

import streamlit as st
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.chat_models import ChatOllama
from langchain.chains import RetrievalQA

sys.path.append(str(Path(__file__).resolve().parent.parent))
from raglib.ingest import extract_text_and_images

# --- Streamlit Setup ---
st.set_page_config(page_title="Document Search Assistant", layout="wide")
with st.sidebar:
    st.title("Document Search Assistant")

# --- Embedding Model ---
embedding_model = "nomic-embed-text"  # Replace with another Ollama embedding model if needed

# --- Container Management ---
with st.sidebar:
    st.subheader("Container")
    container_root = Path("containers")
    container_root.mkdir(exist_ok=True)
    containers = [f.name for f in container_root.iterdir() if f.is_dir()]
    selected_container = st.selectbox("Select container", containers + ["<Create New>"])

    if selected_container == "<Create New>":
        new_container = st.text_input("New container name")
        if st.button("Create Container") and new_container:
            base = container_root / new_container
            (base / "data").mkdir(parents=True, exist_ok=True)
            (base / "chroma_index").mkdir(parents=True, exist_ok=True)
            with open(base / "config.json", "w") as f:
                json.dump({"embedding_model": embedding_model}, f, indent=2)
            st.success(f"Container '{new_container}' created.")
            st.experimental_rerun()
    else:
        container_path = container_root / selected_container
        data_dir = container_path / "data"
        index_dir = container_path / "chroma_index"
        ingested_path = container_path / "ingested_files.json"
        ingested_data = json.load(open(ingested_path)) if ingested_path.exists() else {}

# --- Display Ingested Files ---
if ingested_data:
    st.subheader("Ingested Files")
    for fname, meta in ingested_data.items():
        st.markdown(f"- {fname} (Pages: {meta['pages']}, Ingested: {meta['timestamp']})")

# --- File Upload ---
uploaded_files = st.file_uploader("Upload PDF files", type=["pdf"], accept_multiple_files=True)
if uploaded_files:
    for file in uploaded_files:
        out_path = data_dir / file.name
        if not out_path.exists():
            with open(out_path, "wb") as f:
                f.write(file.getbuffer())
    st.success("File(s) uploaded.")

# --- Ingestion ---
if st.button("Ingest Uploaded Files"):
    embedder = OllamaEmbeddings(model=embedding_model)
    db = Chroma(persist_directory=str(index_dir), embedding_function=embedder)
    splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=100)

    pdfs = [f for f in os.listdir(data_dir) if f.endswith(".pdf")]
    progress = st.progress(0)
    errors = []

    for i, fname in enumerate(pdfs):
        if fname in ingested_data:
            progress.progress((i + 1) / len(pdfs))
            continue
        try:
            pdf_path = str(data_dir / fname)
            docs = extract_text_and_images(pdf_path, image_dir=str(data_dir))
            chunks = splitter.split_documents(docs)
            db.add_documents(chunks)
            db.persist()

            ingested_data[fname] = {
                "timestamp": datetime.now().isoformat(),
                "pages": len(docs)
            }
        except Exception as e:
            errors.append(f"{fname}: {e}")
        progress.progress((i + 1) / len(pdfs))

    with open(ingested_path, "w") as f:
        json.dump(ingested_data, f, indent=2)

    if errors:
        st.error("Some files failed:\n" + "\n".join(errors))
    else:
        st.success("All files ingested.")

# --- Query Interface ---
st.subheader("Ask a Question")
query = st.text_input("Enter your question:")

if query and index_dir.exists():
    embedder = OllamaEmbeddings(model=embedding_model)
    db = Chroma(persist_directory=str(index_dir), embedding_function=embedder)

    llm = ChatOllama(model="mistral", temperature=0.2)
    qa = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=db.as_retriever(search_kwargs={"k": 3}),
        return_source_documents=True
    )

    result = qa(query)
    st.subheader("Answer")
    st.write(result["result"])

    st.subheader("Sources")
    for doc in result["source_documents"]:
        meta = doc.metadata
        st.markdown(f"**{Path(meta.get('source', '')).name}**, Page {meta.get('page')}")
        snippet = doc.page_content[:500] + "..." if len(doc.page_content) > 500 else doc.page_content
        st.markdown(snippet)
