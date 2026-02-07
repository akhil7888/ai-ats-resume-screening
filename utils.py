import streamlit as st
from groq import Groq
from docx import Document
from io import BytesIO
import fitz  # PyMuPDF for PDF

# Initialize Groq client
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# -----------------------------
# GENERIC GROQ LLM CALL
# -----------------------------
def groq_llm(prompt, max_tokens=500):
    try:
        response = client.chat.completions.create(
            model="llama3-8b-8192",     # ✅ Stable model, safer than 70B
            messages=[{"role": "user", "content": prompt}],
            max_tokens=max_tokens,
            temperature=0.0            # deterministic output
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
        text = "\n".join([p.text for p in doc.paragraphs])
        return text

    return ""


# -----------------------------
# ATS SCORE
# -----------------------------
def ats_scores(resume, jd):
    prompt = f"""
    Compare the resume to the job description and give numeric scores only.
    Return strictly JSON:

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
    Provide a detailed ATS analysis comparing resume and job description.

    Resume:
    {resume}

    Job Description:
    {jd}
    """
    return groq_llm(prompt, max_tokens=800)


# -----------------------------
# IMPROVED RESUME
# -----------------------------
def improve_resume(resume, jd):
    prompt = f"""
    Rewrite and improve this resume to match the job description.
    Make it stronger but truthful.

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
    You are an expert resume assistant.
    Answer the question based only on the resume.

    Resume:
    {resume}

    Question: {question}
    """
    return groq_llm(prompt)


# -----------------------------
# JOB DESCRIPTION GENERATOR
# -----------------------------
def generate_job_description(role):
    prompt = f"Generate a professional job description for the role: {role}"
    return groq_llm(prompt)


# -----------------------------
# RECRUITER MODE
# -----------------------------
def recruiter_evaluation(resume):
    prompt = f"""
    As a recruiter, evaluate this resume. Include:

    - Strengths
    - Weaknesses
    - Hiring recommendation

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
