import streamlit as st
import pandas as pd
import re

st.set_page_config(page_title="TalentSpark AI Agent", layout="wide")

st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
    color: white;
}

.title-container {
    background: rgba(255, 255, 255, 0.08);
    padding: 22px;
    border-radius: 18px;
    text-align: center;
    margin-bottom: 25px;
    box-shadow: 0 8px 30px rgba(0,0,0,0.25);
}

.main-title {
    background: -webkit-linear-gradient(#ff7b7b, #ffd1d1);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    font-size: 34px;
    font-weight: 800;
}

h3 {
    color: white !important;
}

.stTextArea textarea {
    background-color: rgba(255,255,255,0.92);
    border-radius: 12px;
}

.stButton > button {
    background: linear-gradient(90deg, #ff4b4b, #ff1a75);
    color: white;
    border-radius: 14px;
    height: 45px;
    width: 180px;
    font-weight: 800;
    font-size: 15px;
    border: none;
    box-shadow: 0 8px 20px rgba(255, 75, 75, 0.35);
}

.winner-card {
    background: rgba(255, 215, 0, 0.12);
    border: 1px solid #ffd700;
    padding: 20px;
    border-radius: 15px;
    text-align: center;
    margin-top: 20px;
}
</style>
""", unsafe_allow_html=True)

st.markdown(
    '<div class="title-container"><div class="main-title">🤖 TalentSpark AI Agent</div></div>',
    unsafe_allow_html=True
)

SKILLS = [
    "python", "java", "javascript", "typescript", "c++", "c#", "go",
    "golang", "rust", "php", "ruby", "swift", "kotlin", "dart",
    "r programming", "scala", "perl", "matlab", "bash", "shell scripting",

    "html", "css", "react", "next.js", "angular", "vue", "svelte", "bootstrap",
    "tailwind", "tailwind css", "material ui", "redux", "jquery",

    "node.js", "express", "django", "flask", "fastapi", "spring boot",
    "spring", "laravel", "rails", "asp.net", ".net", "graphql", "rest api",
    "api development", "microservices",

    "sql", "mysql", "postgresql", "postgres", "mongodb", "redis", "sqlite",
    "oracle", "mssql", "sql server", "firebase", "supabase", "dynamodb",
    "cassandra", "elasticsearch",

    "machine learning", "deep learning", "artificial intelligence", "ai",
    "data science", "data analysis", "nlp", "natural language processing",
    "computer vision", "opencv", "pytorch", "tensorflow", "keras",
    "scikit-learn", "sklearn", "pandas", "numpy", "matplotlib", "seaborn",
    "statistics", "regression", "classification", "clustering", "llm",
    "large language models", "generative ai", "prompt engineering",
    "hugging face", "langchain", "rag", "fine tuning", "model training",

    "etl", "data pipeline", "apache spark", "spark", "hadoop", "kafka",
    "airflow", "databricks", "snowflake", "bigquery", "redshift",

    "aws", "azure", "gcp", "google cloud", "docker", "kubernetes", "jenkins",
    "github actions", "gitlab ci", "ci/cd", "terraform", "ansible", "linux",
    "nginx", "apache", "devops",

    "android", "ios", "flutter", "react native", "swiftui", "xcode",
    "mobile app development",

    "cybersecurity", "ethical hacking", "penetration testing", "networking",
    "network security", "linux security", "owasp", "vulnerability assessment",
    "siem", "soc", "firewall", "cryptography",

    "ui/ux", "ui design", "ux design", "figma", "adobe xd", "photoshop",
    "illustrator", "wireframing", "prototyping", "user research",

    "excel", "power bi", "tableau", "looker", "google analytics",
    "business intelligence", "data visualization", "dashboarding",

    "agile", "scrum", "jira", "product management", "project management",
    "communication", "leadership", "problem solving", "teamwork",

    "git", "github", "gitlab", "bitbucket", "postman", "vs code",
    "linux command line"
]


def extract_text_from_resume(uploaded_file):
    if uploaded_file.name.lower().endswith(".txt"):
        return uploaded_file.read().decode("utf-8", errors="ignore")

    if uploaded_file.name.lower().endswith(".pdf"):
        try:
            from pypdf import PdfReader
        except ImportError:
            st.error("PDF reading needs pypdf. Run: python -m pip install pypdf")
            return ""

        reader = PdfReader(uploaded_file)
        text = ""

        for page in reader.pages:
            text += page.extract_text() or ""

        return text

    return ""


def clean_words(text):
    text = text.lower()
    text = re.sub(r"[^a-zA-Z0-9+#./ ]", " ", text)
    return set(word for word in text.split() if len(word) > 2)


def find_skills(text):
    text = text.lower()
    text = re.sub(r"\s+", " ", text)

    found_skills = []

    for skill in SKILLS:
        skill_lower = skill.lower()
        escaped_skill = re.escape(skill_lower)

        pattern = (
            r"(?<![a-zA-Z0-9])"
            + escaped_skill.replace(r"\ ", r"\s+")
            + r"(?![a-zA-Z0-9])"
        )

        if re.search(pattern, text):
            found_skills.append(skill)

    return found_skills


def guess_candidate_name(file_name, resume_text):
    lines = [line.strip() for line in resume_text.splitlines() if line.strip()]

    if lines:
        first_line = lines[0]
        if len(first_line.split()) <= 5:
            return first_line

    return file_name.rsplit(".", 1)[0].replace("_", " ").replace("-", " ").title()


def calculate_resume_scores(jd_text, resume_text):
    jd_skills = find_skills(jd_text)
    resume_skills = find_skills(resume_text)

    matched_skills = [skill for skill in jd_skills if skill in resume_skills]
    missing_skills = [skill for skill in jd_skills if skill not in resume_skills]

    jd_words = clean_words(jd_text)
    resume_words = clean_words(resume_text)
    matched_keywords = sorted(list(jd_words.intersection(resume_words)))

    skill_score = 0
    if jd_skills:
        skill_score = (len(matched_skills) / len(jd_skills)) * 60

    keyword_score = min(25, len(matched_keywords) * 2)
    resume_depth_score = 15 if len(resume_text.split()) > 120 else 8

    match_score = int(min(95, skill_score + keyword_score + resume_depth_score))
    interest_score = int(min(90, 55 + len(matched_skills) * 7 + len(matched_keywords[:5]) * 2))

    if matched_skills:
        explanation = f"Resume matches required skills: {', '.join(matched_skills[:6])}."
    else:
        explanation = "Limited direct skill match found. Some general JD keywords may overlap."

    return match_score, interest_score, matched_skills, missing_skills, explanation


def build_outreach(candidate_name, matched_skills, missing_skills, match_score):
    matched_text = ", ".join(matched_skills[:4]) if matched_skills else "very few required skills"
    missing_text = ", ".join(missing_skills[:4]) if missing_skills else "no major missing requirement"

    if match_score >= 75:
        fit_status = "Strong fit"
        decision = "Recommended to proceed for recruiter outreach."
        interest_note = "Likely interested because the resume strongly matches the role requirements."
    elif match_score >= 55:
        fit_status = "Moderate fit"
        decision = "Can be considered, but recruiter should verify missing skills first."
        interest_note = "May be interested, but the fit is not complete."
    else:
        fit_status = "Not a good fit"
        decision = "Not recommended to proceed for this role."
        interest_note = "Interest is likely low because the resume does not match key JD requirements."

    return f"""
- **Fit Status:** {fit_status}
- **Candidate Message:** Hi {candidate_name}, we compared your resume with this role.
- **Matched Skills:** {matched_text}
- **Missing Skills:** {missing_text}
- **Interest Insight:** {interest_note}
- **Recruiter Decision:** {decision}
"""


col1, col2 = st.columns([1, 1], gap="large")

with col1:
    st.markdown("### 📋 Job Description")
    jd_input = st.text_area("Paste JD here", height=250, label_visibility="collapsed")

with col2:
    st.markdown("### 📄 Resume Upload")
    uploaded_resumes = st.file_uploader(
        "Upload one or more resumes",
        type=["pdf", "txt"],
        accept_multiple_files=True
    )

    st.markdown("### 🚀 Operation")
    scout_btn = st.button("FIND TALENT")


if scout_btn:
    if not jd_input:
        st.warning("Please enter a Job Description first!")
    elif not uploaded_resumes:
        st.warning("Please upload at least one resume PDF or TXT file!")
    else:
        st.info("Parsing job description...")
        st.info("Reading resume text...")
        st.info("Matching candidate profile with JD...")
        st.info("Simulating recruiter outreach and interest detection...")

        results = []
        progress_bar = st.progress(0)

        for index, resume_file in enumerate(uploaded_resumes):
            progress_bar.progress((index + 1) / len(uploaded_resumes))

            resume_text = extract_text_from_resume(resume_file)

            if not resume_text.strip():
                continue

            candidate_name = guess_candidate_name(resume_file.name, resume_text)

            match_score, interest_score, matched_skills, missing_skills, explanation = calculate_resume_scores(
                jd_input,
                resume_text
            )

            outreach = build_outreach(candidate_name, matched_skills, missing_skills, match_score)

            results.append({
                "Candidate": candidate_name,
                "Match Score": match_score,
                "Interest Score": interest_score,
                "Matched Skills": ", ".join(matched_skills) if matched_skills else "None",
                "Missing Skills": ", ".join(missing_skills) if missing_skills else "None",
                "Explanation": explanation,
                "Simulated Outreach": outreach
            })

        if not results:
            st.error("Could not read resume text. Try uploading a text-based PDF or TXT resume.")
        else:
            df = pd.DataFrame(results)
            df["Final Rank Score"] = (df["Match Score"] + df["Interest Score"]) / 2
            df = df.sort_values(by="Final Rank Score", ascending=False)

            st.success("Ranked shortlist ready!")

            st.markdown(
                f'<div class="winner-card"><h2 style="color: #ffd700;">⭐ Top Pick: {df.iloc[0]["Candidate"]}</h2></div>',
                unsafe_allow_html=True
            )

            st.write("### 📊 Ranked Shortlist")
            st.dataframe(df, use_container_width=True)

            st.write("### 💬 Simulated Outreach")
            for _, row in df.iterrows():
                with st.expander(f"Outreach for {row['Candidate']}"):
                    st.markdown(row["Simulated Outreach"])