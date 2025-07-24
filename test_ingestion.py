# test_ingestion.py

import unittest
from ingestion import clean_text # Import the function we want to test

class TestCleanText(unittest.TestCase):
    """
    A suite of tests for the clean_text function.
    """

    def test_removes_extra_newlines_and_spaces(self):
        """
        Tests if the function correctly handles multiple newlines and spaces.
        """
        # 1. Define the sample input and the expected output
        dirty_text = "This   is a test.\n\nIt has extra spaces\nand newlines."
        expected_output = "This is a test. It has extra spaces and newlines."

        # 2. Call the function with the sample input
        actual_output = clean_text(dirty_text)

        # 3. Assert that the actual output matches the expected output
        self.assertEqual(actual_output, expected_output)

    def test_handles_already_clean_text(self):
        """
        Tests if the function doesn't change text that is already clean.
        """
        clean_input = "This is perfectly clean text."
        expected_output = "This is perfectly clean text."

        actual_output = clean_text(clean_input)

        self.assertEqual(actual_output, expected_output)

    def test_with_leading_and_trailing_spaces(self):
        """
        Tests if leading and trailing whitespace is correctly removed.
        """
        messy_input = "    some text with spaces at the end    "
        expected_output = "some text with spaces at the end"

        actual_output = clean_text(messy_input)

        self.assertEqual(actual_output, expected_output)