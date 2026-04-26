# TalentSpark AI Agent

TalentSpark AI Agent is a Streamlit-based recruiting assistant that helps recruiters screen resumes faster.

## Problem Statement

Recruiters spend hours reviewing profiles and chasing candidate interest. TalentSpark AI Agent helps automate this workflow by taking a Job Description and uploaded resumes, matching candidates against the role, estimating interest, and producing a ranked shortlist.

## What It Does

The app takes a Job Description and one or more uploaded resumes. It extracts resume text, detects skills, compares candidate profiles with the JD, calculates Match Score and Interest Score, simulates recruiter outreach, and outputs a ranked shortlist.

## Features

- Job Description input
- Resume upload in PDF/TXT format
- Resume text extraction
- Skill and keyword matching
- Match Score calculation
- Interest Score calculation
- Matched skills and missing skills
- Explainability for scores
- Simulated recruiter outreach
- Ranked shortlist with top candidate

## Tech Stack

- Python
- Streamlit
- Pandas
- PyPDF
- Regular Expressions

## How To Run Locally

Install dependencies:

```bash
pip install -r requirements.txt

## Run the app
python -m streamlit run app.py

## Architecture
Recruiter
   ↓
Job Description Input
   ↓
Resume Upload
   ↓
PDF/TXT Text Extraction
   ↓
Skill and Keyword Matching
   ↓
Match Score + Interest Score
   ↓
Simulated Outreach
   ↓
Ranked Shortlist

Scoring Logic
The app calculates Match Score using three factors:
Skill Match: compares required JD skills with resume skills
Keyword Overlap: checks common important words between JD and resume
Resume Depth: gives extra weight to resumes with enough detail
The Interest Score is simulated using matched skills and keyword overlap. It estimates how likely a candidate may be interested based on how closely their profile aligns with the role.

Final Rank Score:
Final Rank Score = (Match Score + Interest Score) / 2
Simulated Outreach
The app generates a recruiter-style outreach summary for every candidate. It classifies candidates as:

Strong fit
Moderate fit
Not a good fit
This helps recruiters quickly decide whether to proceed.

Sample Input
We are hiring a Python Machine Learning Engineer with SQL, NLP, and data analysis experience. The candidate should be able to build AI models and work with large datasets.
Sample Output
The app returns:

Candidate name
Match Score
Interest Score
Matched Skills
Missing Skills
Explanation
Simulated Outreach
Final Rank Score

## Demo Video
[Watch Demo Video](https://www.loom.com/share/073af22f045b4dca8cdabc866b949fc4)

## Live App
[Open Live App](https://talentspark-ai-agent-bg4yz39zwrjxmexrpp8ytu.streamlit.app)
