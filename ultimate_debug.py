# find_text.py

import logging
import re

SOURCE_TXT_FILE = "documents/NVIDIA_source.txt"
# A smaller, unique part of the sentence to search for
SEARCH_SNIPPET = "data center growth was fueled by"

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

def main():
    logging.info(f"--- Searching for snippet in {SOURCE_TXT_FILE} ---")

    try:
        with open(SOURCE_TXT_FILE, 'r', encoding='utf-8') as f:
            full_text = f.read()
    except Exception as e:
        logging.error(f"Could not read the text file. Error: {e}")
        return

    # Use regex to find the full sentence containing the snippet
    # This pattern looks for a sentence ending with a period.
    match = re.search(r'([^.]*' + re.escape(SEARCH_SNIPPET) + r'[^.]*\.)', full_text, re.IGNORECASE)

    if match:
        found_sentence = match.group(1).strip()
        logging.info("✅✅✅ SUCCESS! Found the sentence. ✅✅✅")
        print("\n--- Here is the EXACT text from your file ---")
        print(found_sentence)
        print("\nNOTE: Please use this exact text as the 'golden_answer' in the evaluation scripts.")
    else:
        logging.error("❌ FAILURE: Even the small snippet could not be found. The text is not in the file.")

if __name__ == '__main__':
    main()