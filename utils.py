import io
from groq import Groq
from pdfminer.high_level import extract_text as pdf_extract
from docx import Document
import json
import streamlit as st

client = Groq(api_key=st.secrets["GROQ_API_KEY"])


# -------------------------
# EXTRACT TEXT
# -------------------------
def extract_text(file):
    if file.name.endswith(".pdf"):
        return pdf_extract(file)
    elif file.name.endswith(".docx"):
        doc = Document(file)
        return "\n".join([p.text for p in doc.paragraphs])
    return ""


# -------------------------
# SAFE AI GENERATOR
# -------------------------
def groq_generate(prompt):
    response = client.chat.completions.create(
        model="mixtral-8x7b-32768",     # SAFE MODEL
        messages=[{"role": "user", "content": prompt}],
        max_tokens=1024,
        temperature=0.4,
    )
    return response.choices[0].message["content"]


# -------------------------
# ATS SCORE CALCULATOR
# -------------------------
def ats_scores(resume, jd):
    prompt = f"""
    Compare the resume to the job description and give only JSON:

    {{
        "match": 75,
        "fit": 80,
        "quality": 70
    }}

    Resume:
    {resume}

    Job Description:
    {jd}
    """
    try:
        return json.loads(groq_generate(prompt))
    except:
        return {"match": 70, "fit": 70, "quality": 70}


def analyze_resume(resume, jd):
    prompt = f"""
    Provide ATS analysis in professional bullet points.

    Resume:
    {resume}

    Job Description:
    {jd}
    """
    return groq_generate(prompt)


def improve_resume(resume, jd):
    prompt = f"""
    Rewrite the resume to better match the job description.
    Make it ATS-friendly and impactful.
    Do NOT add fake information.

    Resume:
    {resume}

    Job Description:
    {jd}
    """
    return groq_generate(prompt)


def generate_job_description(role):
    prompt = f"Write a professional job description for role: {role}"
    return groq_generate(prompt)


def recruiter_evaluation(resume):
    prompt = f"Act as a recruiter. Give strengths, weaknesses, and hire/no-hire decision.\nResume:\n{resume}"
    return groq_generate(prompt)


def chat_about_resume(resume, question):
    prompt = f"""
    You answer based ONLY on this resume:
    {resume}

    Question:
    {question}
    """
    return groq_generate(prompt)
