# Resume Screening and Ranking System

This project automatically screens resumes for a given job role. It cleans resume text, extracts skills, compares candidates with the job description, ranks them, and shows missing required skills.

## Project Structure

```text
resume-screening-system/
  backend/
    app.py                  Flask API
  frontend/
    index.html              Browser UI
    styles.css              Frontend styling
    script.js               Frontend API logic
  ml/
    text_processing.py      Text cleaning, tokenization, stop-word handling
    skill_extractor.py      Skill library, role skill map, skill matching
    resume_ranker.py        Scoring and ranking model
    sample_run.py           Quick command-line demo
  data/
    sample_job.txt
    sample_resumes.json
  notebooks/
    resume_screening_demo.ipynb
  requirements.txt
```

## How To Run

Open PowerShell in this folder:

```powershell
cd "$env:USERPROFILE\Desktop\resume-screening-system"
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python -m spacy download en_core_web_sm
python -m nltk.downloader stopwords
```

Start the backend:

```powershell
python backend\app.py
```

The API runs at:

```text
http://127.0.0.1:5057
```

Open the frontend:

```text
frontend\index.html
```

Use **Load Sample**, then **Rank Candidates**. The page sends the job role, job description, and resume text to the Flask API.

## Quick ML Demo

```powershell
python -m ml.sample_run
```

## How The System Works

### 1. Text Cleaning

Raw resumes contain emails, phone numbers, punctuation, links, inconsistent spacing, and mixed casing. `ml/text_processing.py` normalizes text by:

- converting text to lowercase
- removing URLs, email addresses, and phone-like strings
- replacing punctuation with spaces
- reducing repeated whitespace

This makes matching more reliable. For example, `Scikit-Learn`, `scikit learn`, and `SCIKIT LEARN` become easier to compare.

### 2. Tokenization And Stop Words

Tokenization splits text into useful word units. Stop words are common words such as `the`, `and`, `to`, and `with`. They usually do not help decide whether a candidate fits a role.

The project tries to use spaCy for lemmatization. Lemmatization converts words to their base form, such as `models` to `model`. If spaCy or its English model is not installed, the system still works using a regex tokenizer and a small fallback stop-word list.

### 3. Skill Extraction

`ml/skill_extractor.py` contains:

- `DEFAULT_SKILLS`: a skill vocabulary
- `ROLE_SKILL_MAP`: common required skills for selected roles
- `extract_skills()`: checks whether known skills appear in the text
- `required_skills_from_job()`: combines role-based skills with skills found in the job description

This approach is explainable. You can see exactly why a candidate matched or missed a skill.

### 4. Feature Extraction With TF-IDF

`ml/resume_ranker.py` uses Scikit-learn's `TfidfVectorizer`.

TF-IDF means **Term Frequency-Inverse Document Frequency**:

- Term Frequency: words that appear often in a document become more important.
- Inverse Document Frequency: words that appear everywhere become less important.

The system converts the job description and each resume into numeric vectors. It then uses cosine similarity to measure how close the resume is to the job description.

### 5. Resume Scoring

The final score combines two signals:

```text
final score = 70% skill match + 30% text similarity
```

Skill match is weighted higher because hiring screens often care most about required skills. Text similarity adds context from the full resume and job description.

### 6. Candidate Ranking

Each candidate receives:

- final score
- recommendation label
- matched skills
- missing required skills
- skill match percentage
- text similarity percentage

Candidates are sorted from highest score to lowest score.

## Improving The Model

Good next improvements:

- Add more skills to `DEFAULT_SKILLS`.
- Expand `ROLE_SKILL_MAP` for your target jobs.
- Parse `.docx` resumes with `python-docx`.
- Train a supervised ranking model if you have historical hiring decisions.
- Add named entity recognition to extract education, companies, and years of experience.
- Store candidate results in a database.

## Important Note

This is a learning project and should assist human review, not replace it. Resume screening systems can reflect bias if the skill list, examples, or scoring weights are poorly chosen. Always audit the results and keep a human decision-maker in the loop.
