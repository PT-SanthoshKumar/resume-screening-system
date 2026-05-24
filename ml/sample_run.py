from resume_ranker import rank_candidates


if __name__ == "__main__":
    role = "Data Scientist"
    job_description = (
        "We need a Data Scientist with Python, SQL, machine learning, statistics, "
        "pandas, scikit learn, data visualization, and model deployment experience."
    )

    resumes = [
        {
            "name": "Aisha Khan",
            "text": "Python data scientist with SQL, pandas, numpy, scikit learn, statistics, and dashboard experience.",
        },
        {
            "name": "Rahul Sharma",
            "text": "Frontend developer skilled in HTML, CSS, JavaScript, React, and API integrations.",
        },
    ]

    print(f"Role: {role}\nJob Description: {job_description}\n")
    print("Results:")
    for candidate in rank_candidates(role, job_description, resumes):
        print(f"Name: {candidate['name']}")
        print(f"  Score: {candidate['score']}")
        print(f"  Matched Skills: {candidate['matched_skills']}")
        print(f"  Missing Skills: {candidate['missing_skills']}")
        print(f"  Skill Match %: {candidate['skill_match_percent']}")
        print(f"  Text Similarity %: {candidate['text_similarity_percent']}")
        print(f"  Recommendation: {candidate['recommendation']}\n")
