import re
import spacy
from src import logger

nlp = spacy.load("en_core_web_sm")


class ResumeInfoExtractor:

    @staticmethod
    def extract_email(text: str):
        email_pattern = r"[a-zA-Z0-9+_.-]+@[a-zA-Z0-9.-]+"
        emails = re.findall(email_pattern, text)
        return emails[0] if emails else None

    @staticmethod
    def extract_phone(text: str):
        phone_pattern = r"\+?\d[\d -]{8,12}\d"
        phones = re.findall(phone_pattern, text)
        return phones[0] if phones else None

    @staticmethod
    def extract_name_location(text: str):

        lines = text.strip().split("\n")

        # Heuristic: First non-empty short line is name
        possible_name = None
        for line in lines:
            line = line.strip()
            if line and len(line.split()) <= 4 and "@" not in line and not any(char.isdigit() for char in line):
                possible_name = line
                break

        clean_text = " ".join(text.split())
        doc = nlp(clean_text)

        location = None
        for ent in doc.ents:
            if ent.label_ in ["GPE", "LOC"]:
                location = ent.text
                break

        return possible_name, location


    @staticmethod
    def extract_all(text: str):

        logger.info("Extracting resume information")

        email = ResumeInfoExtractor.extract_email(text)
        phone = ResumeInfoExtractor.extract_phone(text)
        name, location = ResumeInfoExtractor.extract_name_location(text)

        return {
            "name": name,
            "email": email,
            "phone": phone,
            "location": location
        }
