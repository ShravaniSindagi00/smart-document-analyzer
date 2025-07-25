# Approach Explanation: A Two-Step "Connected" RAG Pipeline

## The Vision: Reimagining Research

The "Connecting the Dots" challenge inspired us to move beyond a simple document search engine and build a true research companion. Our core insight is that effective research is not a brute-force activity; it’s a two-step process of first identifying the most relevant chapters and then reading the details within them. Our solution is engineered to mimic this intelligent, human-centric approach.

We have built an integrated system that connects our Round 1A and 1B solutions into a single, cohesive pipeline. This creates a "Connected RAG" architecture that is both faster and more accurate than a standard implementation.

---

## Our Two-Step Search Methodology

Our system's innovation lies in its two-stage search process, which directly addresses the hackathon's theme:

**1. Coarse-Grained Search (Using the 1A Outline):**
Instead of immediately performing a detailed search across every word of every document, our system first runs our Round 1A header extraction logic. This provides a structured, high-level outline (Title, H1s, H2s) for each PDF in the collection. We then perform a rapid semantic search on the text of these **headings**. This acts as a "smart filter," allowing the system to instantly identify the most relevant major sections across all documents that are likely to contain the answer.

**2. Fine-Grained Search (Using the 1B Pipeline):**
Once the most promising high-level sections are identified, our system proceeds to the detailed analysis. It uses the page numbers from the Round 1A outline to focus the powerful Round 1B RAG pipeline on a much smaller, more relevant set of text chunks. This targeted approach prevents the system from being distracted by irrelevant information, dramatically improving the accuracy and relevance of the final ranked results.

---

## Why This Approach is Superior

By "connecting the dots" between the document's structure and its content, our system offers two key advantages:

* **Enhanced Relevance**: By focusing the search on pre-qualified sections, we significantly increase the signal-to-noise ratio, leading to a higher quality ranking of the final extracted sections.
* **Greater Efficiency**: Performing a detailed semantic search on a smaller, targeted set of text is computationally faster and more efficient than searching through the entire document collection.

Our solution is more than just a tool that finds text; it’s a system that understands context and prioritizes information in a way that feels intelligent and intuitive, truly embodying the spirit of the "Connecting the Dots" challenge.