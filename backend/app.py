import os
import sys
from pathlib import Path

from flask import Flask, jsonify, request
from flask_cors import CORS

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(PROJECT_ROOT))

from ml.resume_ranker import rank_candidates  # noqa: E402


app = Flask(__name__)
CORS(app)


def _read_uploaded_file(file_storage) -> str:
    filename = (file_storage.filename or "").lower()
    raw = file_storage.read()

    if filename.endswith(".txt"):
        return raw.decode("utf-8", errors="ignore")

    if filename.endswith(".pdf"):
        try:
            import io
            from PyPDF2 import PdfReader

            reader = PdfReader(io.BytesIO(raw))
            return "\n".join(page.extract_text() or "" for page in reader.pages)
        except Exception as exc:
            raise ValueError(f"Could not read PDF file {file_storage.filename}: {exc}") from exc

    return raw.decode("utf-8", errors="ignore")


@app.get("/api/health")
def health():
    return jsonify({"status": "ok"})


@app.post("/api/rank")
def rank_from_json():
    payload = request.get_json(force=True, silent=True) or {}
    role = payload.get("role", "")
    job_description = payload.get("job_description", "")
    resumes = payload.get("resumes", [])

    if not role or not job_description or not resumes:
        return jsonify({"error": "role, job_description, and resumes are required"}), 400

    return jsonify({
        "role": role,
        "results": rank_candidates(role, job_description, resumes),
    })


@app.post("/api/rank-files")
def rank_from_files():
    role = request.form.get("role", "")
    job_description = request.form.get("job_description", "")
    files = request.files.getlist("resumes")

    if not role or not job_description or not files:
        return jsonify({"error": "role, job_description, and at least one resume file are required"}), 400

    resumes = []
    try:
        for file_storage in files:
            resumes.append({
                "name": os.path.splitext(file_storage.filename)[0],
                "text": _read_uploaded_file(file_storage),
            })
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400

    return jsonify({
        "role": role,
        "results": rank_candidates(role, job_description, resumes),
    })


if __name__ == "__main__":
    port = int(os.environ.get("RESUME_API_PORT", "5057"))
    app.run(debug=True, host="127.0.0.1", port=port)
