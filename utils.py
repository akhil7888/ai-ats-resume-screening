import streamlit as st
from groq import Groq
from docx import Document
from io import BytesIO
import fitz  # PyMuPDF


# -----------------------------
# INIT GROQ CLIENT
# -----------------------------
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# FINAL PERMANENT MODEL
MODEL = "gemma2-9b-it"


def groq_llm(prompt, max_tokens=800):
    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.1,
            max_tokens=max_tokens
        )
        return response.choices[0].message.content.strip()

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
# ATS SCORES
# -----------------------------
def ats_scores(resume, jd):
    prompt = f"""
    Compare the resume and job description.
    Return ONLY JSON:
    {{
        "match": 0-100,
        "fit": 0-100,
        "quality": 0-100
    }}
    Resume:
    {resume}

    Job Description:
    {jd}
    """

    result = groq_llm(prompt)

    try:
        return eval(result)
    except:
        return {"match": 75, "fit": 75, "quality": 75}


# -----------------------------
# ATS ANALYSIS
# -----------------------------
def analyze_resume(resume, jd):
    prompt = f"""
    Provide detailed ATS analysis of strengths, weaknesses,
    missing skills and suggestions.

    Resume:
    {resume}

    Job Description:
    {jd}
    """
    return groq_llm(prompt, max_tokens=1200)


# -----------------------------
# IMPROVED RESUME
# -----------------------------
def improve_resume(resume, jd):
    prompt = f"""
    Improve this resume to match the job description.
    Keep it truthful, professional and short.

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
    Answer the question ONLY using resume information.

    Resume:
    {resume}

    Question:
    {question}
    """
    return groq_llm(prompt, max_tokens=600)


# -----------------------------
# JD GENERATOR
# -----------------------------
def generate_job_description(role):
    return groq_llm(f"Generate a full professional job description for: {role}", max_tokens=600)


# -----------------------------
# RECRUITER MODE
# -----------------------------
def recruiter_evaluation(resume):
    prompt = f"""
    Evaluate this resume like a recruiter.
    Provide strengths, weaknesses and hiring recommendation.

    Resume:
    {resume}
    """
    return groq_llm(prompt, max_tokens=700)


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
