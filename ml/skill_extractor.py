from typing import Dict, Iterable, List

from .text_processing import clean_text, contains_phrase, unique_preserve_order


DEFAULT_SKILLS = [
    "python", "java", "sql", "machine learning", "deep learning", "nlp",
    "natural language processing", "scikit learn", "tensorflow", "pytorch",
    "pandas", "numpy", "matplotlib", "seaborn", "flask", "django", "fastapi",
    "api", "git", "docker", "aws", "azure", "gcp", "linux", "statistics",
    "data analysis", "data visualization", "excel", "power bi", "tableau",
    "communication", "problem solving", "leadership", "project management",
    "html", "css", "javascript", "react", "node", "mongodb", "postgresql",
    "spark", "hadoop", "etl", "airflow", "feature engineering", "model deployment",
]


ROLE_SKILL_MAP: Dict[str, List[str]] = {
    "data scientist": [
        "python", "sql", "machine learning", "statistics", "pandas", "numpy",
        "scikit learn", "data visualization", "feature engineering", "model deployment",
    ],
    "machine learning engineer": [
        "python", "machine learning", "deep learning", "scikit learn", "pytorch",
        "tensorflow", "docker", "api", "model deployment", "aws",
    ],
    "nlp engineer": [
        "python", "nlp", "natural language processing", "machine learning",
        "deep learning", "spacy", "pytorch", "tensorflow", "model deployment",
    ],
    "data analyst": [
        "sql", "excel", "python", "pandas", "data analysis", "data visualization",
        "power bi", "tableau", "statistics", "communication",
    ],
    "frontend developer": [
        "html", "css", "javascript", "react", "api", "git", "problem solving",
    ],
    "backend developer": [
        "python", "java", "sql", "api", "flask", "django", "fastapi", "docker",
        "postgresql", "git",
    ],
}


def skills_for_role(role: str) -> List[str]:
    return ROLE_SKILL_MAP.get(clean_text(role), [])


def extract_skills(text: str, skill_library: Iterable[str] = None) -> List[str]:
    skill_library = unique_preserve_order(skill_library or DEFAULT_SKILLS)
    matched = []
    for skill in skill_library:
        if contains_phrase(text, skill):
            matched.append(skill)
    return matched


def required_skills_from_job(role: str, job_description: str) -> List[str]:
    role_skills = skills_for_role(role)
    jd_skills = extract_skills(job_description, DEFAULT_SKILLS)
    return unique_preserve_order(role_skills + jd_skills)

