# final_debug.py (v2 - Corrected)

import logging
import fitz  # PyMuPDF
import re

# --- CONFIGURATION ---
PDF_FILE_PATH = "documents/NVIDIAAn.pdf"
GOLDEN_ANSWER = "Our data center growth was fueled by strong and accelerating demand for generative Al training and inference on the Hopper platform."
# ---------------------

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

def normalize_text(text):
    """Removes extra whitespace and newlines to make searching more robust."""
    return re.sub(r'\s+', ' ', text).strip()

def main():
    logging.info(f"--- STARTING FINAL DEBUG (v2) for {PDF_FILE_PATH} ---")
    
    # 1. Directly extract text from the single PDF using PyMuPDF
    try:
        doc = fitz.open(PDF_FILE_PATH)
        full_text = ""
        for page in doc:
            full_text += page.get_text()
        doc.close()
        logging.info("Step 1: Successfully extracted text with PyMuPDF.")
    except Exception as e:
        logging.error(f"Failed to read the PDF file at {PDF_FILE_PATH}. Error: {e}")
        return
        
    # 2. Check for the golden answer in the raw text
    if GOLDEN_ANSWER in full_text:
        logging.info("Step 2: ✅ SUCCESS. The golden answer IS PRESENT in the raw extracted text.")
    else:
        logging.warning("Step 2: ⚠️ The exact golden answer was NOT found in the raw text. This is common. Proceeding to a more robust check...")

        # 3. Perform a more robust "normalized" check
        normalized_full_text = normalize_text(full_text)
        normalized_golden_answer = normalize_text(GOLDEN_ANSWER)

        if normalized_golden_answer in normalized_full_text:
            logging.info("Step 3: ✅ SUCCESS. The golden answer WAS FOUND after normalizing the text.")
            logging.info("This confirms the text is being extracted, but with formatting issues. This is fixable.")
        else:
            logging.error("Step 3: ❌ FAILURE. The golden answer could not be found even after cleaning the text. The content may be an image or have severe encoding issues.")

if __name__ == '__main__':
    main()



    