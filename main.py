# main.py (v6 - Final Integrated Version with Path Fix)

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

import json
import logging
import datetime
from pathlib import Path

# --- Round 1B Imports ---
from ingestion import process_documents 
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

# --- Round 1A Imports ---
from src.config.settings import Settings
from src.extractor import PDFParser, HeadingDetector, OutlineBuilder

# Set up basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logging.getLogger("pdfminer").setLevel(logging.WARNING)

def run_round_1a_extraction(input_dir: str) -> dict:
    """
    Runs the header extraction logic from Round 1A on all PDFs in a directory.
    Returns a dictionary mapping filenames to their JSON outlines.
    """
    logging.info("--- Running Round 1A: Header Extraction ---")
    outlines = {}
    
    # Initialize 1A components
    app_settings = Settings.load()
    pdf_parser = PDFParser(app_settings)
    heading_detector = HeadingDetector(app_settings)
    outline_builder = OutlineBuilder(app_settings)
    
    pdf_files = [p for p in Path(input_dir).glob("*.pdf")]
    
    for pdf_path in pdf_files:
        try:
            logging.info(f"Extracting outline for: {pdf_path.name}")
            document = pdf_parser.parse(pdf_path)
            headings = heading_detector.detect_headings(document)
            outline = outline_builder.build_outline(headings)
            
            # Store the structured outline
            outlines[pdf_path.name] = {
                "title": document.filename,
                "outline": [{"level": f"H{h.level}", "text": h.text, "page": h.page} for h in outline.headings]
            }
        except Exception as e:
            logging.error(f"Failed to extract outline for {pdf_path.name}: {e}")
            
    logging.info(f"Successfully extracted outlines for {len(outlines)} documents.")
    return outlines

def main():
    """
    Main function for the integrated Round 1A + 1B pipeline.
    """
    # --- Define Folder Paths for Docker / Local ---
    INPUT_DIR = os.environ.get("INPUT_DIR", "input")
    OUTPUT_DIR = os.environ.get("OUTPUT_DIR", "output")


    # --- User Input & Query Processing ---
    user_role = "Investment Analyst"
    user_goal = "Analyze revenue trends, R&D investments, and market positioning strategies"
    search_query = f"As a {user_role}, I need to {user_goal}."
    
    # --- Step 1: Run Round 1A to get document outlines ---
    document_outlines = run_round_1a_extraction(INPUT_DIR)

    # --- Step 2: Coarse-Grained Search on Headings ---
    logging.info("--- Running Step 2: Coarse-Grained Search on Headings ---")
    
    all_headings = []
    for filename, data in document_outlines.items():
        for heading in data.get("outline", []):
            heading['source_doc'] = filename
            all_headings.append(heading)
    
    heading_texts = [h['text'] for h in all_headings]
    embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    
    vector_store_headings = Chroma.from_texts(
        texts=heading_texts,
        embedding=embedding_model,
        metadatas=all_headings
    )
    
    relevant_headings = vector_store_headings.similarity_search(search_query, k=5)
    logging.info(f"Found {len(relevant_headings)} potentially relevant major sections.")

    # --- Step 3: Fine-Grained Search within Relevant Sections ---
    all_chunks = process_documents(document_directory=INPUT_DIR)
    if not all_chunks:
        logging.warning("No document chunks processed. Exiting.")
        return

    chunk_texts = [chunk.page_content for chunk in all_chunks]
    vector_store_chunks = Chroma.from_texts(
        texts=chunk_texts,
        embedding=embedding_model,
        metadatas=[chunk.metadata for chunk in all_chunks]
    )

    relevant_docs = vector_store_chunks.similarity_search(search_query, k=10)
    
    # --- Final JSON Output Generation ---
    logging.info("Formatting final output...")
    output_data = {
        "metadata": {
            "input_documents": list(document_outlines.keys()),
            "persona": user_role,
            "job_to_be_done": user_goal,
            "processing_timestamp": datetime.datetime.now().isoformat(),
            "connected_dots_strategy": {
                "description": "Used Round 1A outlines to first find relevant major sections before performing a detailed search.",
                "top_sections_found": [doc.metadata for doc in relevant_headings]
            }
        },
        "extracted_sections": []
    }

    for i, doc in enumerate(relevant_docs):
        section = {
            "document": doc.metadata.get("source", "Unknown"),
            "page_number": doc.metadata.get("page", -1),
            "importance_rank": i + 1,
            "refined_text": doc.page_content,
            "section_title": doc.page_content[:100] + "..."
        }
        output_data["extracted_sections"].append(section)

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    output_filename = os.path.join(OUTPUT_DIR, "output.json")
    with open(output_filename, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, indent=4)

    logging.info(f"✅✅✅ Success! Integrated analysis complete. Output written to {output_filename} ✅✅✅")


if __name__ == '__main__':
    main()