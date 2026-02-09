import io
from groq import Groq
from pdfminer.high_level import extract_text as pdfminer_extract
from docx import Document
import json
import streamlit as st

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# -------------------------
# EXTRACT TEXT FROM PDF/DOCX
# -------------------------
def extract_text(uploaded_file):
    if uploaded_file.type == "application/pdf":
        return pdfminer_extract(uploaded_file)

    elif uploaded_file.type in [
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        "application/msword",
    ]:
        doc = Document(uploaded_file)
        return "\n".join([para.text for para in doc.paragraphs])

    else:
        return "Unsupported file type"


# -------------------------
# GENERIC GROQ GENERATOR
# -------------------------
def groq_generate(prompt, tokens=1024):
    response = client.chat.completions.create(
        model="mixtral-8x7b-32768",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=tokens,
        temperature=0.2
    )
    return response.choices[0].message["content"]


# -------------------------
# ATS MATCH SCORING
# -------------------------
def ats_scores(resume_text, jd_text):
    prompt = f"""
    Compare the following resume and job description and return a JSON with:
    - ats_match (0-100)
    - job_fit (0-100)
    - resume_quality (0-100)

    Resume:
    {resume_text}

    Job Description:
    {jd_text}

    Return JSON only:
    """
    result = groq_generate(prompt)
    try:
        return json.loads(result)
    except:
        return {"ats_match": 70, "job_fit": 70, "resume_quality": 70}


# -------------------------
# ATS ANALYSIS
# -------------------------
def analyze_resume(resume_text, jd_text):
    prompt = f"""
    Provide a detailed ATS analysis comparing this resume and job description.

    Resume:
    {resume_text}

    Job Description:
    {jd_text}
    """
    return groq_generate(prompt, tokens=2048)


# -------------------------
# IMPROVED RESUME
# -------------------------
def improve_resume(resume_text, jd_text):
    prompt = f"""
    Rewrite and improve the following resume to better match the job description,
    while keeping truth & honesty.

    Resume:
    {resume_text}

    Job Description:
    {jd_text}
    """
    return groq_generate(prompt, tokens=2048)


# -------------------------
# JD GENERATOR
# -------------------------
def generate_job_description(role):
    prompt = f"Generate a professional job description for: {role}"
    return groq_generate(prompt)


# -------------------------
# RECRUITER MODE
# -------------------------
def recruiter_evaluation(resume_text):
    prompt = f"""
    Act like a senior recruiter. Evaluate this resume, list strengths,
    weaknesses, hiring decision, and give hiring recommendation.

    Resume:
    {resume_text}
    """
    return groq_generate(prompt)


# -------------------------
# CHAT WITH RESUME
# -------------------------
def chat_about_resume(resume_text, question):
    prompt = f"""
    You are an expert career assistant. Use ONLY the resume below to answer.

    Resume: {resume_text}

    Question: {question}
    """
    return groq_generate(prompt)
