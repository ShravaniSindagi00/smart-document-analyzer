# ingestion.py

import os
import re
import fitz  # The PyMuPDF library
from langchain_text_splitters import RecursiveCharacterTextSplitter
import logging

# Set up basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def extract_text_from_pdf(pdf_path):
    """Opens a PDF file and extracts the text from all pages using PyMuPDF."""
    try:
        doc = fitz.open(pdf_path)
        text = ""
        for page in doc:
            text += page.get_text()
        doc.close()
        return text
    except Exception as e:
        logging.error(f"Failed to read text from {pdf_path} with PyMuPDF: {e}")
        return None

def clean_text(text):
    """Cleans the text by removing extra whitespace and special characters."""
    text = re.sub(r'\n+', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def chunk_text(text):
    """Splits the text into smaller chunks."""
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    chunks = text_splitter.split_text(text)
    return chunks

def process_documents(document_directory="documents"):
    """
    Finds all PDFs in a directory, extracts, cleans, and chunks the text.
    Returns a list of all text chunks.
    """
    if not os.path.exists(document_directory):
        logging.error(f"Directory not found: {document_directory}")
        return []

    all_chunks = []
    for filename in os.listdir(document_directory):
        if filename.lower().endswith(".pdf"):
            file_path = os.path.join(document_directory, filename)
            logging.info(f"Processing {file_path}...")

            raw_text = extract_text_from_pdf(file_path)
            if not raw_text:
                continue

            cleaned_text = clean_text(raw_text)
            chunks = chunk_text(cleaned_text)
            all_chunks.extend(chunks)
            logging.info(f"Created {len(chunks)} chunks from {filename}.")

    return all_chunks