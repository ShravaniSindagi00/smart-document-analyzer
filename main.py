# main.py

import logging
from ingestion import process_documents

# New imports for this module
from langchain_huggingface import HuggingFaceEmbeddings 
from langchain_community.vectorstores import Chroma

# Set up basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def main():
    """
    Main function to run the smart document analyzer.
    """
    # --- 3.3 User Input & Query Processing ---
    user_role = "a business analyst"
    user_goal = "find the latest research on company profits"
    search_query = f"As {user_role}, I need to {user_goal}."
    logging.info(f"Transformed user input into search query: '{search_query}'")

    # --- 3.2 Data Ingestion & Preprocessing ---
    logging.info("Starting document ingestion and processing...")
    all_text_chunks = process_documents()

    if not all_text_chunks:
        logging.warning("No documents processed. Exiting.")
        return
    logging.info(f"Successfully processed documents into {len(all_text_chunks)} chunks.")
    
    # --- 3.4 Information Retrieval Module ---

    # 1. Integrate Embedding Model (WBS 3.4.1)
    # We use a popular, efficient model from Hugging Face.
    logging.info("Initializing embedding model...")
    embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    
    # 2. Implement Vector Store Management (WBS 3.4.2)
    # We create a ChromaDB vector store from the document chunks.
    # This will automatically handle embedding each chunk and storing it.
    logging.info("Creating vector store from document chunks...")
    vector_store = Chroma.from_texts(texts=all_text_chunks, embedding=embedding_model)

    # 3. Code Semantic Search Function (WBS 3.4.3)
    # We perform a similarity search to find the most relevant chunks.
    logging.info("Performing semantic search...")
    relevant_docs = vector_store.similarity_search(search_query)

    # --- Display Results ---
    logging.info(f"\nFound {len(relevant_docs)} relevant document sections:")
    for i, doc in enumerate(relevant_docs):
        print(f"\n--- Relevant Section {i+1} ---")
        print(doc.page_content)
        print("--------------------------")


if __name__ == '__main__':
    main()