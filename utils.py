import streamlit as st
import fitz  # PyMuPDF
import docx
import re
from docx import Document
from io import BytesIO
from groq import Groq

# Initialize Groq Client
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# -----------------------------------------------------
# TEXT EXTRACTION
# -----------------------------------------------------
def extract_text(file):
    if file.name.endswith(".pdf"):
        pdf = fitz.open(stream=file.read(), filetype="pdf")
        text = ""
        for page in pdf:
            text += page.get_text()
        return text

    elif file.name.endswith(".docx"):
        doc = docx.Document(file)
        return "\n".join([p.text for p in doc.paragraphs])

    return ""

# -----------------------------------------------------
# DETERMINISTIC ATS SCORE (Stable)
# -----------------------------------------------------
def deterministic_score(text, jd_text):
    text = text.lower()
    jd_text = jd_text.lower()

    jd_keywords = re.findall(r"\b[a-zA-Z]+\b", jd_text)
    resume_words = re.findall(r"\b[a-zA-Z]+\b", text)

    overlap = len(set(jd_keywords) & set(resume_words))
    total = len(set(jd_keywords))

    if total == 0:
        return 0

    return int((overlap / total) * 100)


def ats_scores(resume_text, jd_text):
    score = deterministic_score(resume_text, jd_text)

    return {
        "match": score,
        "fit": min(score + 5, 100),
        "quality": min(score + 10, 100)
    }

# -----------------------------------------------------
# AI GENERATION (GROQ)
# -----------------------------------------------------
def groq_generate(prompt):
    response = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
        max_tokens=1200
    )
    return response.choices[0].message["content"]


def analyze_resume(resume, jd):
    prompt = f"""
You are an ATS expert. Analyze the resume against the job description.

Resume:
{resume}

Job Description:
{jd}

Provide a structured ATS analysis.
"""
    return groq_generate(prompt)


def improve_resume(resume, jd):
    prompt = f"""
Rewrite this resume to improve ATS match. Keep it realistic and professional.

Resume:
{resume}

Job Description:
{jd}
"""
    return groq_generate(prompt)


def chat_about_resume(resume_text, question):
    prompt = f"""
Resume:
{resume_text}

Question: {question}

Answer in detail using resume content only.
"""
    return groq_generate(prompt)


def generate_job_description(role):
    prompt = f"Generate a professional job description for the role: {role}"
    return groq_generate(prompt)


def recruiter_evaluation(resume):
    prompt = f"""
You are a recruiter. Evaluate this resume in 4 parts:

1. Summary
2. Strengths
3. Weaknesses
4. Hire / No-hire decision

Resume:
{resume}
"""
    return groq_generate(prompt)


# -----------------------------------------------------
# EXPORT PDF
# -----------------------------------------------------
def export_pdf(text):
    buffer = BytesIO()
    doc = fitz.open()

    page = doc.new_page()
    page.insert_text((50, 50), text, fontsize=12)

    doc.save(buffer)
    buffer.seek(0)
    return buffer


# -----------------------------------------------------
# EXPORT DOCX
# -----------------------------------------------------
def export_docx(text):
    doc = Document()
    for line in text.split("\n"):
        doc.add_paragraph(line)

    buffer = BytesIO()
    doc.save(buffer)
    buffer.seek(0)
    return buffer
