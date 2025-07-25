Here’s a cleaner, more concise, and professional-style `README.md` without emojis or bullet-heavy formatting — more suitable for submissions like Adobe’s Hackathon:

---

# Smart Document Analyzer – Adobe India Hackathon 2025

**Round 1A & 1B Integrated Solution – "Connecting the Dots"**

This project provides a unified and intelligent solution for Adobe’s “Connecting the Dots” Hackathon challenge. It combines document structural understanding (Round 1A) with persona-driven contextual search (Round 1B) to deliver meaningful and accurate results tailored to user intent.

## Overview

Our system goes beyond keyword search. It first analyzes the document’s high-level structure to extract key sections (like chapters or headings). Then, it performs semantic search only within those relevant segments — ensuring speed, precision, and alignment with user goals.

This two-stage, retrieval-augmented system is containerized for easy deployment, runs offline, and meets all hackathon constraints.

## Key Features

* **Two-Stage Search Pipeline**
  The system first identifies major document sections using structural analysis (Round 1A), then applies semantic search (Round 1B) within these regions.

* **Persona-Centric Output**
  Responses are customized based on the user’s persona and specific goals (e.g., a student preparing for an exam).

* **End-to-End RAG Pipeline**
  Fully local, Retrieval-Augmented Generation pipeline powered by LangChain and HuggingFace Transformers.

* **Precise Traceability**
  Each result includes exact document source and page number for full transparency.

* **Dockerized Execution**
  Secure, portable, and reproducible setup using Docker.

## Tech Stack

* **Language**: Python 3.10
* **PDF Processing**: PyMuPDF (text extraction), Pytesseract (OCR)
* **RAG Orchestration**: LangChain
* **Embeddings**: `all-MiniLM-L6-v2` (from Hugging Face)
* **Vector DB**: ChromaDB
* **Containerization**: Docker

## How to Use

### 1. Prerequisites

* Install Docker and ensure it is running.

### 2. Add Input PDFs

Place 3–10 PDF files in the `/input` folder at the root of the project.

### 3. Build the Docker Image

```bash
docker build --platform linux/amd64 -t smart-analyzer-integrated:latest .
```

### 4. Run the Application

```bash
docker run --rm -v ./input:/app/input -v ./output:/app/output smart-analyzer-integrated:latest
```

### 5. View Output

After processing, the results will be saved to:

```
/output/output.json
```

This file contains a list of relevant document sections based on the query and user persona, with source details.

---

Let me know if you want to include a "Project Structure" or "Example Output" section as well.
