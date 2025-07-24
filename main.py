# main.py

import logging
from ingestion import process_documents

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

# New imports for the generation module
from transformers import pipeline

# Set up basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def format_context(docs):
    """Helper function to format the retrieved documents into a single string."""
    context = ""
    for i, doc in enumerate(docs):
        context += f"--- Relevant Section {i+1} ---\n"
        context += doc.page_content
        context += "\n--------------------------\n\n"
    return context

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
    logging.info("Initializing embedding model...")
    embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    
    logging.info("Creating vector store from document chunks...")
    vector_store = Chroma.from_texts(texts=all_text_chunks, embedding=embedding_model)

    logging.info("Performing semantic search...")
    relevant_docs = vector_store.similarity_search(search_query)

    # --- 3.5 Reranking & Generation Module ---
    
    # 1. Prepare context and build the prompt
    context = format_context(relevant_docs)
    prompt_template = f"""
    You are a helpful assistant for a {user_role}. Your task is to answer the user's question based *only* on the provided context.
    
    User's Goal: {user_goal}

    Context from documents:
    {context}
    
    Based on the context above, please provide a concise answer to help the user achieve their goal.
    Answer:
    """
    
    # 2. Integrate LLM and generate the final answer
    logging.info("Initializing text generation model...")
    # Using a smaller, efficient model for local execution
    generator = pipeline('text-generation', model='distilgpt2')

    logging.info("Generating final answer...")
    final_answer = generator(prompt_template, max_length=500, num_return_sequences=1)

    # --- Display Final Answer ---
    print("\n\n✅ ================== FINAL ANSWER ================== ✅")
    print(final_answer[0]['generated_text'])
    print("========================================================")


if __name__ == '__main__':
    main()