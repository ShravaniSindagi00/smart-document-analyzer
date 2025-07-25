
````markdown
# Smart Document Analyzer - Adobe India Hackathon 2025

## Challenge: Round 1 - Integrated Document Intelligence

This project is a complete, integrated solution for Round 1 of the "Connecting the Dots" challenge. It combines the structured outline extraction from Round 1A with the persona-driven analysis of Round 1B to create a single, intelligent system.

The application processes a collection of PDFs, understands their structure, and then extracts and ranks the most relevant sections based on a specific user persona and their goal.

### Core Features

* **Integrated "Connecting the Dots" Logic**: Uniquely combines the structured outline extraction (Round 1A) with the persona-driven search (Round 1B). The system first identifies relevant major sections using the document's headings and then performs a detailed analysis, making it faster and more accurate.
* **Intelligent RAG Pipeline**: Implements a full Retrieval-Augmented Generation (RAG) pipeline to perform semantic search on documents.
* **Persona-Driven Analysis**: Tailors the search and ranking based on a provided user role and their specific objective.
* **Source Tracking**: Accurately identifies the source document and page number for every extracted piece of information.
* **Dockerized for Submission**: The entire application is containerized with Docker, ensuring a consistent and reproducible execution environment as required by the hackathon rules.

---

### Technology Stack

* **Language**: Python 3.10
* **Core Libraries**:
    * `PyMuPDF` & `pdfminer.six`: For robust PDF text and structure extraction.
    * `LangChain`: As the primary framework for orchestrating the RAG pipeline.
    * `Hugging Face Transformers`: For accessing state-of-the-art, local embedding models (`all-MiniLM-L6-v2`).
    * `ChromaDB`: As the in-memory vector database for efficient semantic search.
    * `Pytesseract`: For OCR capabilities in the Round 1A header extraction.

---

### How to Build and Run the Solution

**Prerequisites:**
* Docker must be installed and running on your system.

**Step 1: Place Input PDFs**

Place the collection of 3-10 PDF documents that you want to analyze into the `/input` folder at the root of this project.

**Step 2: Build the Docker Image**

Open a terminal in the root directory of the project and run the following command. This will build the Docker image, installing all necessary dependencies inside the container.

```bash
docker build --platform linux/amd64 -t smart-analyzer-integrated:latest .
````

**Step 3: Run the Application**

After the image is successfully built, run the following command. This will start the container, which will automatically process the PDFs from the `/input` folder and generate the final analysis in the `/output` folder.

```bash
docker run --rm -v ./input:/app/input -v ./output:/app/output smart-analyzer-integrated:latest
```

**Step 4: View the Result**

Once the container finishes execution, a new file named `output.json` will appear in your `/output` folder. This file contains the final, ranked list of relevant sections in the format specified by the hackathon rules.

```
```