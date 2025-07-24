# main.py

import logging
from ingestion import process_documents

# Set up basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def main():
    """
    Main function to run the smart document analyzer.
    """
    # --- 3.3 Build User Input & Query Processing Module ---

    # 1. Simulate user input (WBS 3.3.1)
    # In the future, this will come from a user interface.
    user_role = "a business analyst"
    user_goal = "find the latest research on company profits"

    # 2. Transform the input into an effective query (WBS 3.3.2)
    # We combine the role and goal into a clear, detailed question for the system.
    search_query = f"As {user_role}, I need to {user_goal}."
    
    logging.info(f"Transformed user input into search query: '{search_query}'")

    # --- 3.2 Build Data Ingestion & Preprocessing Module ---
    # We call the function from our ingestion script to get the document chunks.
    logging.info("Starting document ingestion and processing...")
    all_text_chunks = process_documents()

    if not all_text_chunks:
        logging.warning("No documents processed. Exiting.")
        return

    logging.info(f"Successfully processed documents into {len(all_text_chunks)} chunks.")
    
    # The next step will be to use the 'search_query' to search through 'all_text_chunks'.


if __name__ == '__main__':
    main()