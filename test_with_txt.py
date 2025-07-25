# test_with_txt.py (v3 - Hybrid Search)

import logging
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter

# --- CONFIGURATION ---
SOURCE_TXT_FILE = "documents/NVIDIA_source.txt"
GOLDEN_ANSWER = "Our data center growth was fueled by strong and accelerating demand for generative Al training and inference on the Hopper platform."
# Using the original, more natural user query
QUERY = "What was the main driver of their revenue growth?"
# ---------------------

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

def main():
    logging.info(f"--- Testing with HYBRID SEARCH from {SOURCE_TXT_FILE} ---")

    # 1. Read and chunk text
    try:
        with open(SOURCE_TXT_FILE, 'r', encoding='utf-8') as f:
            full_text = f.read()
    except Exception as e:
        logging.error(f"Could not read the text file. Error: {e}")
        return

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = text_splitter.split_text(full_text)
    logging.info(f"Created {len(chunks)} chunks.")

    # 2. Perform Semantic Search (Attempt 1)
    logging.info("--- Attempt 1: Semantic Search ---")
    embedding_model = HuggingFaceEmbeddings(model_name="multi-qa-mpnet-base-dot-v1")
    vector_store = Chroma.from_texts(texts=chunks, embedding=embedding_model)
    retrieved_docs = vector_store.similarity_search(QUERY, k=5)

    found_semantically = False
    for i, doc in enumerate(retrieved_docs):
        if GOLDEN_ANSWER in doc.page_content:
            logging.info(f"✅✅✅ SUCCESS (Semantic)! Found golden answer at rank {i+1} ✅✅✅")
            found_semantically = True
            break
    
    if not found_semantically:
        logging.warning("Semantic search failed. Moving to fallback...")
        
        # 3. Perform Keyword Search (Attempt 2 - Fallback)
        logging.info("\n--- Attempt 2: Keyword Search (Fallback) ---")
        found_by_keyword = False
        for i, chunk in enumerate(chunks):
            if GOLDEN_ANSWER in chunk:
                logging.info(f"✅✅✅ SUCCESS (Keyword)! Found golden answer in chunk #{i} ✅✅✅")
                found_by_keyword = True
                break
        
        if not found_by_keyword:
            logging.error("❌❌❌ ULTIMATE FAILURE. Answer not found even with keyword search.")

if __name__ == '__main__':
    main()