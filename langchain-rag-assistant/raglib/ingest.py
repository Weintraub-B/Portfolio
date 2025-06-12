import os
import fitz  # PyMuPDF
import logging
from pathlib import Path
from langchain_core.documents import Document
from langchain_community.vectorstores.utils import filter_complex_metadata

# Logger setup
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

if not logger.handlers:
    handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

def extract_text_and_images(pdf_path: str, image_dir: str) -> list:
    """
    Extracts clean text and any embedded images from the PDF.
    Returns a list of LangChain Document objects with sanitized metadata.
    """
    documents = []
    pdf_name = Path(pdf_path).stem
    image_dir = Path(image_dir)
    image_dir.mkdir(parents=True, exist_ok=True)

    doc = fitz.open(pdf_path)

    for page_number, page in enumerate(doc, start=1):
        text = page.get_text().strip()
        image_paths = []

        for idx, img in enumerate(page.get_images(full=True)):
            xref = img[0]
            try:
                pix = fitz.Pixmap(doc, xref)
                if pix.n not in (1, 3):
                    pix = fitz.Pixmap(fitz.csRGB, pix)
                img_path = image_dir / f"{pdf_name}_p{page_number}_{idx}.png"
                pix.save(str(img_path))
                image_paths.append(str(img_path))
            except Exception as e:
                logger.warning(f"Image save failed on page {page_number}: {e}")

        metadata = filter_complex_metadata({
            "source": pdf_path,
            "page": page_number,
            "images": image_paths
        })

        documents.append(Document(page_content=text, metadata=metadata))

    logger.info(f"Extracted {len(documents)} pages from '{Path(pdf_path).name}'")
    return documents
