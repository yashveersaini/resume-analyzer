from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from src.core.embeddings import encode_text
from src import logger

from src.core.skill_extractor import SkillExtractor


class ResumeMatcher:

    @staticmethod
    def calculate_ats_score(resume_text: str, job_description: str):

        # -------- Semantic Similarity --------
        resume_embedding = encode_text(resume_text)
        job_embedding = encode_text(job_description)

        similarity_score = cosine_similarity(
            [resume_embedding],
            [job_embedding]
        )[0][0]

        semantic_score = float(similarity_score) * 100

        # -------- Skill Matching --------
        resume_skills = SkillExtractor.extract_skills(resume_text)
        job_skills = SkillExtractor.extract_skills(job_description)

        if job_skills:
            matched_skills = set(resume_skills) & set(job_skills)
            skill_score = (len(matched_skills) / len(job_skills)) * 100
        else:
            skill_score = 0

        # -------- Final Hybrid Score --------
        final_score = float((0.6 * semantic_score) + (0.4 * skill_score))

        return {
            "semantic_score": round(semantic_score, 2),
            "skill_match_score": round(skill_score, 2),
            "final_ats_score": round(final_score, 2),
            "matched_skills": list(set(resume_skills) & set(job_skills)),
            "missing_skills": list(set(job_skills) - set(resume_skills))
        }
