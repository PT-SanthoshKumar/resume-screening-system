const API_URL = "http://127.0.0.1:5057/api/rank";

const roleInput = document.querySelector("#roleInput");
const jobInput = document.querySelector("#jobInput");
const resumeList = document.querySelector("#resumeList");
const results = document.querySelector("#results");
const statusText = document.querySelector("#statusText");
const resultCount = document.querySelector("#resultCount");

const sampleData = {
  role: "Data Scientist",
  job: "We need a Data Scientist with Python, SQL, machine learning, statistics, pandas, scikit learn, data visualization, feature engineering, and model deployment experience.",
  resumes: [
    {
      name: "Aisha Khan",
      text: "Data Scientist with Python, SQL, pandas, numpy, scikit learn, statistics, feature engineering, dashboards, and model deployment using Flask."
    },
    {
      name: "Rahul Sharma",
      text: "Frontend Developer with HTML, CSS, JavaScript, React, API integration, Git, and responsive UI experience."
    },
    {
      name: "Meera Patel",
      text: "Data Analyst with SQL, Excel, Tableau, Power BI, Python, pandas, data analysis, statistics, and communication skills."
    }
  ]
};

function createResumeCard(name = "", text = "") {
  const card = document.createElement("div");
  card.className = "resume-card";
  card.innerHTML = `
    <div class="resume-card-header">
      <input class="resume-name" type="text" placeholder="Candidate name" value="${escapeHtml(name)}">
      <button class="remove-btn" type="button">Remove</button>
    </div>
    <textarea class="resume-text" rows="7" placeholder="Paste resume text here...">${escapeHtml(text)}</textarea>
  `;

  card.querySelector(".remove-btn").addEventListener("click", () => card.remove());
  resumeList.appendChild(card);
}

function getResumes() {
  return [...document.querySelectorAll(".resume-card")].map((card, index) => ({
    name: card.querySelector(".resume-name").value.trim() || `Candidate ${index + 1}`,
    text: card.querySelector(".resume-text").value.trim()
  })).filter((resume) => resume.text);
}

function escapeHtml(value) {
  return String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}

function renderChips(items, className = "") {
  if (!items.length) return `<span class="chip ${className}">None</span>`;
  return items.map((item) => `<span class="chip ${className}">${escapeHtml(item)}</span>`).join("");
}

function renderResults(candidates) {
  resultCount.textContent = `${candidates.length} candidate${candidates.length === 1 ? "" : "s"}`;
  results.className = "";
  results.innerHTML = candidates.map((candidate, index) => `
    <article class="result-card">
      <div class="result-topline">
        <div>
          <h2>${index + 1}. ${escapeHtml(candidate.name)}</h2>
          <span class="recommendation">${escapeHtml(candidate.recommendation)}</span>
        </div>
        <div class="score">${candidate.score}%</div>
      </div>
      <div class="metric-row">
        <span class="metric">Skill match: ${candidate.skill_match_percent}%</span>
        <span class="metric">Text similarity: ${candidate.text_similarity_percent}%</span>
      </div>
      <div class="skill-section">
        <strong>Matched skills</strong>
        <div class="chip-row">${renderChips(candidate.matched_skills)}</div>
      </div>
      <div class="skill-section">
        <strong>Missing required skills</strong>
        <div class="chip-row">${renderChips(candidate.missing_skills, "missing")}</div>
      </div>
    </article>
  `).join("");
}

async function rankCandidates() {
  const payload = {
    role: roleInput.value.trim(),
    job_description: jobInput.value.trim(),
    resumes: getResumes()
  };

  if (!payload.role || !payload.job_description || !payload.resumes.length) {
    statusText.textContent = "Add a role, job description, and at least one resume.";
    return;
  }

  statusText.textContent = "Ranking candidates...";
  try {
    const response = await fetch(API_URL, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    });
    const data = await response.json();
    if (!response.ok) throw new Error(data.error || "Ranking failed");
    renderResults(data.results);
    statusText.textContent = "Ranking complete.";
  } catch (error) {
    statusText.textContent = `${error.message}. Start the Flask backend and try again.`;
  }
}

document.querySelector("#addResumeBtn").addEventListener("click", () => createResumeCard());
document.querySelector("#rankBtn").addEventListener("click", rankCandidates);
document.querySelector("#loadSampleBtn").addEventListener("click", () => {
  roleInput.value = sampleData.role;
  jobInput.value = sampleData.job;
  resumeList.innerHTML = "";
  sampleData.resumes.forEach((resume) => createResumeCard(resume.name, resume.text));
});

createResumeCard();
