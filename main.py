# main.py (v3 - Final JSON Output)

import os
import json
import logging
import datetime
from ingestion import process_documents # Our upgraded ingestion script

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

# Set up basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def main():
    """
    Main function to run the smart document analyzer and generate JSON output.
    """
    # --- User Input & Query Processing ---
    # These would come from the hackathon's test case runner
    user_role = "Investment Analyst"
    user_goal = "Analyze revenue trends, R&D investments, and market positioning strategies"
    search_query = f"As a {user_role}, I need to {user_goal}."
    
    input_documents = [f for f in os.listdir("documents") if f.endswith('.pdf')]

    logging.info("Starting document analysis...")
    logging.info(f"User Role: {user_role}")
    logging.info(f"User Goal: {user_goal}")
    
    # --- Data Ingestion & Preprocessing ---
    # This now returns a list of DocumentChunk objects with metadata
    all_chunks = process_documents()

    if not all_chunks:
        logging.warning("No documents processed. Exiting.")
        return
    logging.info(f"Successfully processed {len(input_documents)} documents into {len(all_chunks)} chunks.")
    
    # --- Information Retrieval Module ---
    # We now pass the page_content of our objects to the vector store
    chunk_texts = [chunk.page_content for chunk in all_chunks]
    
    logging.info("Initializing embedding model...")
    embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    
    logging.info("Creating vector store...")
    # The vector store needs the metadata to be attached to the texts
    vector_store = Chroma.from_texts(
        texts=chunk_texts, 
        embedding=embedding_model,
        # We pass the metadata from our DocumentChunk objects here
        metadatas=[chunk.metadata for chunk in all_chunks] 
    )

    logging.info("Performing semantic search...")
    # The search will now return documents with our attached metadata
    relevant_docs = vector_store.similarity_search(search_query, k=10) # Get top 10 relevant chunks

    # --- Generate JSON Output ---
    logging.info("Formatting output into required JSON structure...")

    output_data = {
        "metadata": {
            "input_documents": input_documents,
            "persona": user_role,
            "job_to_be_done": user_goal,
            "processing_timestamp": datetime.datetime.now().isoformat()
        },
        "extracted_sections": []
    }

    for i, doc in enumerate(relevant_docs):
        section = {
            "document": doc.metadata.get("source", "Unknown"),
            "page_number": doc.metadata.get("page", -1),
            "importance_rank": i + 1,
            "refined_text": doc.page_content,
            # For this round, we can consider the refined text as the "section title"
            "section_title": doc.page_content[:100] + "..." # Truncate for a title
        }
        output_data["extracted_sections"].append(section)

    # Write the output to a JSON file
    output_filename = "output.json"
    with open(output_filename, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, indent=4)

    logging.info(f"✅✅✅ Success! Output written to {output_filename} ✅✅✅")


if __name__ == '__main__':
    main()