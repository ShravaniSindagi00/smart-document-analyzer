# ingestion.py (v3 - With Source Tracking)

import os
import re
import fitz  # PyMuPDF
from langchain_text_splitters import RecursiveCharacterTextSplitter
import logging

# Set up basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class DocumentChunk:
    """A custom class to hold chunk data and its source metadata."""
    def __init__(self, page_content, document_name, page_number):
        self.page_content = page_content
        self.metadata = {
            "source": document_name,
            "page": page_number
        }
    
    def __repr__(self):
        return f"DocumentChunk(source='{self.metadata['source']}', page={self.metadata['page']})"

def process_documents(document_directory="documents"):
    """
    Finds all PDFs in a directory, extracts text, and returns a list of DocumentChunk objects.
    """
    if not os.path.exists(document_directory):
        logging.error(f"Directory not found: {document_directory}")
        return []

    all_chunks = []
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )

    for filename in os.listdir(document_directory):
        if filename.lower().endswith(".pdf"):
            file_path = os.path.join(document_directory, filename)
            logging.info(f"Processing {file_path}...")
            
            try:
                doc = fitz.open(file_path)
                for page_num, page in enumerate(doc):
                    text = page.get_text()
                    if not text:
                        continue
                    
                    # Clean the text before chunking
                    cleaned_text = re.sub(r'\s+', ' ', text).strip()
                    
                    chunks = text_splitter.split_text(cleaned_text)
                    for chunk_text in chunks:
                        # For each chunk, create our custom object with metadata
                        chunk_obj = DocumentChunk(
                            page_content=chunk_text,
                            document_name=filename,
                            page_number=page_num + 1 # Page numbers are 1-based
                        )
                        all_chunks.append(chunk_obj)
                doc.close()
                logging.info(f"Created chunks for {filename}.")
            except Exception as e:
                logging.error(f"Failed to process {file_path}: {e}")
            
    return all_chunks