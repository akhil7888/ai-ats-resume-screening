import io
from groq import Groq
from pdfminer.high_level import extract_text
from docx import Document
import streamlit as st
import json

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# -----------------------------
# Extract text from PDF or DOCX
# -----------------------------
def extract_resume_text(file):
    if file.type == "application/pdf":
        return extract_text(io.BytesIO(file.read()))
    else:
        doc = Document(file)
        return "\n".join(p.text for p in doc.paragraphs)

# -----------------------------
# Generate using Groq
# -----------------------------
def groq_generate(prompt, model):
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=1200,
        temperature=0.2
    )
    return response.choices[0].message.content

# -----------------------------
# ATS scoring
# -----------------------------
def ats_scores(resume_text, jd_text):
    prompt = f"""
    Evaluate the resume against the Job Description.

    Return JSON with:
    - match: %
    - fit: %
    - quality: %

    Resume:
    {resume_text}

    JD:
    {jd_text}
    """

    output = groq_generate(prompt, st.secrets["GROQ_MODEL_ATS"])
    try:
        return json.loads(output)
    except:
        return {"match": 70, "fit": 70, "quality": 70}

# -----------------------------
# Analyze Resume
# -----------------------------
def analyze_resume(resume_text, jd_text):
    prompt = f"""
    Provide ATS analysis of this resume vs job description.
    Resume:
    {resume_text}

    JD:
    {jd_text}
    """

    return groq_generate(prompt, st.secrets["GROQ_MODEL_ATS"])

# -----------------------------
# Improve Resume
# -----------------------------
def improve_resume(resume_text, jd_text):
    prompt = f"""
    Rewrite this resume to better match the job description while keeping truthful.

    Resume:
    {resume_text}

    JD:
    {jd_text}
    """

    return groq_generate(prompt, st.secrets["GROQ_MODEL_ATS"])

# -----------------------------
# Chat with Resume
# -----------------------------
def chat_about_resume(resume_text, question):
    prompt = f"""
    You are a resume assistant.
    Answer based ONLY on this resume:

    Resume:
    {resume_text}

    Question: {question}
    """

    return groq_generate(prompt, st.secrets["GROQ_MODEL_CHAT"])
