# evaluation.py

import os
import logging
from ingestion import process_documents
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

# NOTE: This is a simplified representation of your golden dataset.
# In a real-world scenario, you would parse this from the PDF files.
GOLDEN_DATASET = [
    # Data from Doc1(financial).pdf
    {
        "user_goal": "What was NVIDIA's total revenue for the first quarter of fiscal year 2025?",
        "golden_answer": "NVIDIA (NASDAQ: NVDA) today reported revenue for the first quarter ended April 28, 2024, of $26.0 billion, up 18% from the previous quarter and up 262% from a year ago."
    },
    {
        "user_goal": "What was the main driver of their revenue growth?",
        "golden_answer": "Our data center growth was fueled by strong and accelerating demand for generative Al training and inference on the Hopper platform."
    },
    # Data from Doc3(academic).pdf
    {
        "user_goal": "What is the definition of a public cloud?",
        "golden_answer": "A public cloud is owned and operated by third-party service providers like Amazon AWS, Google Cloud, or Microsoft Azure."
    },
    {
        "user_goal": "Why would an organization choose to use a private cloud instead of a public one?",
        "golden_answer": "They are best for companies that deal with sensitive data, such as banks, healthcare, and government agencies."
    }
]

# Set up basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def calculate_mrr(dataset, vector_store):
    """
    Calculates the Mean Reciprocal Rank for the retrieval system.
    """
    reciprocal_ranks = []
    
    for item in dataset:
        query = item["user_goal"]
        golden_answer = item["golden_answer"]
        
        logging.info(f"Evaluating query: '{query}'")
        
        # Retrieve the top 5 most relevant documents for the query
        retrieved_docs = vector_store.similarity_search(query, k=5)
        
        rank = 0
        found = False
        for i, doc in enumerate(retrieved_docs):
            # Check if the golden answer is present in the retrieved chunk
            if golden_answer in doc.page_content:
                rank = i + 1
                found = True
                break
        
        if found:
            reciprocal_rank = 1 / rank
            logging.info(f"Found golden answer at rank {rank}. Reciprocal Rank = {reciprocal_rank:.2f}")
        else:
            reciprocal_rank = 0
            logging.info("Golden answer not found in top 5 results. Reciprocal Rank = 0")
            
        reciprocal_ranks.append(reciprocal_rank)
        
    # Calculate the mean of all reciprocal ranks
    mrr = sum(reciprocal_ranks) / len(reciprocal_ranks) if reciprocal_ranks else 0
    return mrr


def main():
    """
    Main function to run the evaluation.
    """
    logging.info("Starting evaluation...")
    
    # 1. Ingest and process the source documents
    all_text_chunks = process_documents()
    if not all_text_chunks:
        logging.error("No documents found to process in 'documents' folder. Exiting.")
        return
        
    # 2. Create the vector store
    embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    vector_store = Chroma.from_texts(texts=all_text_chunks, embedding=embedding_model)
    
    # 3. Calculate and print the MRR
    logging.info("Calculating MRR...")
    mrr_score = calculate_mrr(GOLDEN_DATASET, vector_store)
    
    print("\n\n✅ ================== EVALUATION RESULT ================== ✅")
    print(f"Mean Reciprocal Rank (MRR): {mrr_score:.4f}")
    print("=========================================================")


if __name__ == '__main__':
    main()