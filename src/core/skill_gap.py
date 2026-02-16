from src.core.skill_extractor import SkillExtractor


class SkillGapAnalyzer:

    @staticmethod
    def analyze(resume_text: str, job_description: str):

        resume_skills = SkillExtractor.extract_skills(resume_text)
        job_skills = SkillExtractor.extract_skills(job_description)

        missing_skills = list(set(job_skills) - set(resume_skills))

        return {
            "resume_skills": resume_skills,
            "job_required_skills": job_skills,
            "missing_skills": missing_skills
        }
