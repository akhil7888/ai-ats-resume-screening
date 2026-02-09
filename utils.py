import io
import json
from docx import Document
from groq import Groq
import pdfminer.high_level as pdfminer


def load_api_key():
    import os
    return os.getenv("GROQ_API_KEY")


client = Groq(api_key=load_api_key())


# --------------------------------
# TEXT EXTRACTION
# --------------------------------
def extract_text(file):
    if file is None:
        return ""

    mime = file.mime_type

    # PDF
    if mime == "application/pdf":
        output = io.StringIO()
        pdfminer.extract_text_to_fp(file, output)
        return output.getvalue()

    # DOCX
    elif mime == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        doc = Document(file)
        return "\n".join([p.text for p in doc.paragraphs])

    return ""
    

# --------------------------------
# GROQ GENERATION WRAPPER
# --------------------------------
def groq_generate(prompt, tokens=600):
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=tokens,
    )
    return response.choices[0].message["content"]


# --------------------------------
# ATS SCORES
# --------------------------------
def ats_scores(resume, jd):
    prompt = f"""
    Evaluate the resume against job description.
    Return JSON only:
    {{
        "match": <number>,
        "fit": <number>,
        "quality": <number>
    }}

    Resume:
    {resume}

    Job Description:
    {jd}
    """

    try:
        result = groq_generate(prompt, 200)
        return json.loads(result)
    except:
        return {"match": 70, "fit": 70, "quality": 70}


# --------------------------------
# ANALYSIS
# --------------------------------
def analyze_resume(resume, jd):
    prompt = f"""
    Perform ATS keyword analysis.
    Provide missing keywords, strengths, weaknesses.

    Resume:
    {resume}

    Job Description:
    {jd}
    """
    return groq_generate(prompt)


# --------------------------------
# IMPROVED RESUME
# --------------------------------
def improve_resume(resume, jd):
    prompt = f"""
    Rewrite the resume to better match job description.
    Keep format clean & professional.

    Resume:
    {resume}

    Job Description:
    {jd}
    """
    return groq_generate(prompt, 800)


# --------------------------------
# JOB DESCRIPTION GENERATOR
# --------------------------------
def generate_jd(role):
    prompt = f"Write a complete job description for the role: {role}"
    return groq_generate(prompt)


# --------------------------------
# RECRUITER MODE
# --------------------------------
def recruiter_evaluation(resume):
    prompt = f"""
    Act as a senior recruiter.
    Evaluate this resume professionally.

    Resume:
    {resume}
    """
    return groq_generate(prompt)


# --------------------------------
# CHAT WITH RESUME
# --------------------------------
def chat_with_resume(resume, question):
    prompt = f"""
    Answer using the resume information only.

    Resume:
    {resume}

    Question: {question}
    """
    return groq_generate(prompt)
