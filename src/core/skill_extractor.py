import re
from src.core.skills_db import TECH_SKILLS
from src import logger


class SkillExtractor:

    @staticmethod
    def normalize_text(text: str):
        text = text.lower()
        text = re.sub(r"[^\w\s\-]", " ", text)
        return text

    @staticmethod
    def extract_skills(text: str):
        logger.info("Extracting skills from text")

        text = SkillExtractor.normalize_text(text)

        found_skills = []

        for skill in TECH_SKILLS:
            if skill in text:
                found_skills.append(skill)

        logger.info(f"Skills found: {found_skills}")

        return list(set(found_skills))
