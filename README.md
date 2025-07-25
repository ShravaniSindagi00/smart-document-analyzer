🚀 Smart Document Analyzer
Adobe India Hackathon 2025 - "Connecting the Dots"
Challenge Solution: Round 1 (Integrated 1A & 1B)
This project is a comprehensive and intelligent solution for Round 1 of the "Connecting the Dots" challenge. It moves beyond a simple search tool by fully integrating the structural analysis of Round 1A with the persona-driven intelligence of Round 1B.
Our system first understands the high-level structure of a document collection and then uses that context to perform a highly relevant, targeted analysis, embodying the hackathon's theme of "Connecting the Dots" to surface meaningful insights.


✨ Core Features & Innovations
"Connected Dots" Architecture: Our key innovation is a two-stage search pipeline. The system first leverages the structured outlines from Round 1A to identify the most relevant major sections (e.g., chapters or headings). It then performs a detailed semantic search (Round 1B) only within these pre-qualified sections, resulting in significantly faster and more accurate results.
Persona-Driven Intelligence: The analysis is tailored to a specific user persona and their "job-to-be-done," ensuring the extracted sections are not just relevant to the query, but also to the user's unique perspective.
End-to-End RAG Pipeline: Implements a complete Retrieval-Augmented Generation (RAG) pipeline using a local, offline-first technology stack.
Precise Source Tracking: Every extracted section is meticulously tracked, providing the exact source document and page number for full traceability.
Submission-Ready: The entire application is containerized with Docker, ensuring a secure, reproducible, and easy-to-run solution that meets all hackathon submission requirements.


🛠️ Technology Stack
Language: Python 3.10

PDF Processing:

PyMuPDF: For high-performance text extraction.

Pytesseract: For OCR capabilities.

AI Framework:

LangChain: For orchestrating the core RAG pipeline.

Hugging Face Transformers: For local, on-device AI models.

AI Models:
all-MiniLM-L6-v2: As the sentence-transformer for semantic search embeddings.
Vector Database:
ChromaDB: For efficient, in-memory vector storage and similarity search.


⚙️ How to Build and Run
Prerequisites:
Docker must be installed and running.


1. Place Input PDFs
Add your collection of 3-10 PDF documents into the /input directory at the project's root.


2. Build the Docker Image
From the project's root directory, execute the following command in your terminal:
docker build --platform linux/amd64 -t smart-analyzer-integrated:latest .



3. Run the Application
Once the image is built, run the container with this command. It will mount the necessary folders, process the PDFs, and generate the final output.
docker run --rm -v ./input:/app/input -v ./output:/app/output smart-analyzer-integrated:latest

4. View the Result
After the container finishes, a new file, output.json, will be created in the /output directory. This file contains the ranked list of relevant sections, formatted according to the hackathon specification.
