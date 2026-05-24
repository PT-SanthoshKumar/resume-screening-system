from dataclasses import dataclass, asdict
from typing import Dict, Iterable, List

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from .skill_extractor import DEFAULT_SKILLS, extract_skills, required_skills_from_job
from .text_processing import clean_text


@dataclass
class CandidateResult:
    name: str
    score: float
    matched_skills: List[str]
    missing_skills: List[str]
    skill_match_percent: float
    text_similarity_percent: float
    recommendation: str

    def to_dict(self) -> Dict:
        return asdict(self)


def _recommendation(score: float) -> str:
    if score >= 80:
        return "Strong fit"
    if score >= 60:
        return "Good fit"
    if score >= 40:
        return "Possible fit"
    return "Needs review"


def _text_similarity(job_text: str, resume_text: str) -> float:
    documents = [clean_text(job_text), clean_text(resume_text)]
    if not documents[0] or not documents[1]:
        return 0.0
    vectorizer = TfidfVectorizer(ngram_range=(1, 2), min_df=1)
    matrix = vectorizer.fit_transform(documents)
    return float(cosine_similarity(matrix[0:1], matrix[1:2])[0][0])


def score_candidate(
    role: str,
    job_description: str,
    candidate_name: str,
    resume_text: str,
    skill_library: Iterable[str] = None,
) -> CandidateResult:
    skill_library = list(skill_library or DEFAULT_SKILLS)
    required_skills = required_skills_from_job(role, job_description)
    if not required_skills:
        required_skills = extract_skills(job_description, skill_library)

    resume_skills = extract_skills(resume_text, skill_library)
    matched = [skill for skill in required_skills if skill in resume_skills]
    missing = [skill for skill in required_skills if skill not in resume_skills]

    skill_score = len(matched) / len(required_skills) if required_skills else 0.0
    similarity_score = _text_similarity(f"{role} {job_description}", resume_text)

    final_score = (0.7 * skill_score + 0.3 * similarity_score) * 100

    return CandidateResult(
        name=candidate_name,
        score=round(final_score, 2),
        matched_skills=matched,
        missing_skills=missing,
        skill_match_percent=round(skill_score * 100, 2),
        text_similarity_percent=round(similarity_score * 100, 2),
        recommendation=_recommendation(final_score),
    )


def rank_candidates(role: str, job_description: str, resumes: List[Dict[str, str]]) -> List[Dict]:
    results = [
        score_candidate(
            role=role,
            job_description=job_description,
            candidate_name=resume.get("name") or f"Candidate {index + 1}",
            resume_text=resume.get("text", ""),
        ).to_dict()
        for index, resume in enumerate(resumes)
    ]
    return sorted(results, key=lambda item: item["score"], reverse=True)

