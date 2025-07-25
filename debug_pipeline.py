# debug_pipeline.py

import logging
from ingestion import process_documents, clean_text
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

# The specific data we are debugging
GOLDEN_ANSWER = "Our data center growth was fueled by strong and accelerating demand for generative Al training and inference on the Hopper platform."
QUERY = "What was the main driver of their revenue growth?"
SOURCE_DOCUMENT_FOLDER = "documents" # Make sure only the NVIDIA PDF is in here for this test

# Set up basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def main():
    logging.info("--- STARTING DEBUGGING SCRIPT ---")

    # 1. Process the document and get all chunks
    all_chunks = process_documents(SOURCE_DOCUMENT_FOLDER)
    if not all_chunks:
        logging.error("No chunks were created. Is the source PDF in the 'documents' folder?")
        return

    logging.info(f"Created {len(all_chunks)} chunks from the source document.")

    # 2. Manually search for the golden answer in the chunks
    found_in_any_chunk = False
    for i, chunk in enumerate(all_chunks):
        if GOLDEN_ANSWER in chunk:
            logging.info(f"✅ SUCCESS: Golden Answer was found in Chunk #{i}")
            print("\n--- Matching Chunk Content ---")
            print(chunk)
            print("----------------------------")
            found_in_any_chunk = True
            break
    
    if not found_in_any_chunk:
        logging.error("❌ FAILURE: The complete golden answer sentence was NOT found in any chunk.")
        logging.error("This means the error is happening during PDF text extraction or chunking.")
        # Optional: Print all chunks to inspect them manually
        # for i, chunk in enumerate(all_chunks):
        #     print(f"\n--- Chunk {i} ---")
        #     print(chunk)
        return

    # 3. If found, let's see why the retrieval is failing
    logging.info("\n--- NOW, TESTING THE RETRIEVAL STEP ---")
    embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    vector_store = Chroma.from_texts(texts=all_chunks, embedding=embedding_model)
    
    retrieved_docs = vector_store.similarity_search(QUERY, k=5)
    
    logging.info(f"Top 5 retrieved docs for the query: '{QUERY}'")
    for i, doc in enumerate(retrieved_docs):
        is_match = "✅ Correct" if GOLDEN_ANSWER in doc.page_content else "❌ Incorrect"
        print(f"\n--- Retrieved Doc #{i+1} ({is_match}) ---")
        print(doc.page_content)


if __name__ == '__main__':
    main()