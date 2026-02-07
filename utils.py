import streamlit as st
from groq import Groq
from docx import Document
from io import BytesIO
import fitz   # PyMuPDF for PDF extraction

# -----------------------------
# INIT GROQ CLIENT
# -----------------------------
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# SAFE & SUPPORTED MODEL (2026)
MODEL = "llama3.1-8b-instruct"


# -----------------------------
# GENERIC LLM FUNCTION
# -----------------------------
def groq_llm(prompt, max_tokens=800):
    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=[{"role": "user", "content": prompt}],
            temperature=0,
            max_tokens=max_tokens
        )
        return response.choices[0].message.content

    except Exception as e:
        return f"[Groq API Error] {str(e)}"


# -----------------------------
# TEXT EXTRACTION
# -----------------------------
def extract_text(file):
    if file.type == "application/pdf":
        pdf = fitz.open(stream=file.read(), filetype="pdf")
        text = ""
        for page in pdf:
            text += page.get_text()
        return text

    elif file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        doc = Document(file)
        return "\n".join([p.text for p in doc.paragraphs])

    return ""


# -----------------------------
# ATS SCORE (Stable JSON)
# -----------------------------
def ats_scores(resume, jd):
    prompt = f"""
    Compare the resume to the job description.

    Return ONLY a JSON dict like:
    {{"match": 0-100, "fit": 0-100, "quality": 0-100}}

    Resume:
    {resume}

    Job Description:
    {jd}
    """

    result = groq_llm(prompt, max_tokens=300)

    try:
        return eval(result)
    except:
        return {"match": 75, "fit": 75, "quality": 75}


# -----------------------------
# ATS ANALYSIS
# -----------------------------
def analyze_resume(resume, jd):
    prompt = f"""
    Provide a detailed ATS analysis including:
    - strengths
    - weaknesses
    - missing skills
    - recommendations

    Resume:
    {resume}

    Job Description:
    {jd}
    """
    return groq_llm(prompt, max_tokens=1000)


# -----------------------------
# IMPROVE RESUME
# -----------------------------
def improve_resume(resume, jd):
    prompt = f"""
    Rewrite and improve the resume to match the job description.
    Maintain truthfulness.

    Resume:
    {resume}

    Job Description:
    {jd}
    """
    return groq_llm(prompt, max_tokens=1500)


# -----------------------------
# CHAT ABOUT RESUME
# -----------------------------
def chat_about_resume(resume, question):
    prompt = f"""
    You are an AI assistant. Answer based ONLY on this resume.

    Resume:
    {resume}

    Question: {question}
    """
    return groq_llm(prompt, max_tokens=600)


# -----------------------------
# JOB DESCRIPTION GENERATOR
# -----------------------------
def generate_job_description(role):
    prompt = f"Generate a professional job description for: {role}"
    return groq_llm(prompt)


# -----------------------------
# RECRUITER MODE
# -----------------------------
def recruiter_evaluation(resume):
    prompt = f"""
    Evaluate this resume like an experienced recruiter.
    Provide strengths, weaknesses & hiring recommendation.

    Resume:
    {resume}
    """
    return groq_llm(prompt)


# -----------------------------
# EXPORT PDF
# -----------------------------
def export_pdf(text):
    buffer = BytesIO()
    buffer.write(text.encode("utf-8"))
    buffer.seek(0)
    return buffer


# -----------------------------
# EXPORT DOCX
# -----------------------------
def export_docx(text):
    buffer = BytesIO()
    doc = Document()
    for line in text.split("\n"):
        doc.add_paragraph(line)
    doc.save(buffer)
    buffer.seek(0)
    return buffer
