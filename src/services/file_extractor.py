import os
from PyPDF2 import PdfReader
from flask import current_app
from src import logger


class FileExtractor:

    @staticmethod
    def extract_text_from_pdf(file_path: str) -> str:
        """
        Extract text from PDF file.
        """
        try:
            logger.info(f"Extracting text from file: {file_path}")

            reader = PdfReader(file_path)
            text = ""

            for page in reader.pages:
                text += page.extract_text() or ""

            if not text.strip():
                logger.warning("No text extracted from PDF.")
                raise ValueError("Empty or unreadable PDF.")

            logger.info("Text extraction successful.")
            return text

        except Exception as e:
            logger.error(f"Error extracting text: {str(e)}")
            raise
