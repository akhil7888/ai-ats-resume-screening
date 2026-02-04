import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import os

from utils import (
    extract_text,
    ats_score,
    llm_analysis,
    improve_resume,
    job_fit_score,
    resume_quality_score,
    skill_gap_matrix,
    export_pdf,
    export_docx,
    chat_with_resume,
)

# ============================
# LOAD CSS
# ============================
def load_css():
    if os.path.exists("styles.css"):
        st.markdown("<style>" + open("styles.css").read() + "</style>", unsafe_allow_html=True)
load_css()

# ============================
# HEADER
# ============================
st.markdown("""
<div class='header-container'>
    <h1 class='main-title'>📄 AI ATS Resume Screening</h1>
    <p class='sub-title'>Powered by Groq · Fast · Accurate · Free</p>
</div>
""", unsafe_allow_html=True)

# ============================
# API KEY HANDLING (Groq)
# ============================
api_key = None

try:
    api_key = st.secrets["GROQ_API_KEY"]
except:
    api_key = None

if not api_key:
    api_key = st.text_input("🔐 Enter your GROQ API Key (local only)", type="password")

if not api_key:
    st.warning("Please enter Groq API Key to continue.")
    st.stop()

# ============================
# FILE UPLOAD
# ============================
resume_file = st.file_uploader("📄 Upload Resume", type=["pdf", "docx", "pptx"])
jd_text = st.text_area("🧾 Paste Job Description", height=180)

if st.button("🔍 Analyze Resume"):

    if not resume_file or not jd_text.strip():
        st.error("Upload resume and paste job description first.")
        st.stop()

    resume_text = extract_text(resume_file)

    st.session_state.resume_text = resume_text
    st.session_state.jd_text = jd_text

    score, missing = ats_score(resume_text, jd_text)
    job_fit = job_fit_score(resume_text, jd_text)
    quality = resume_quality_score(resume_text)
    skill_matrix = skill_gap_matrix(resume_text, jd_text)

    st.markdown("## 📊 ATS Overview")
    c1, c2, c3 = st.columns(3)
    c1.metric("ATS Match", f"{score}%")
    c2.metric("Job Fit", f"{job_fit}%")
    c3.metric("Quality", f"{quality}%")

    st.markdown("### ⭐ ATS Score")
    st.markdown(
        f"<div class='score-bar'><div class='score-fill' style='width:{score}%;'></div></div>",
        unsafe_allow_html=True,
    )

    radar = go.Figure()
    radar.add_trace(go.Scatterpolar(
        r=[score, job_fit, quality],
        theta=["ATS Match", "Job Fit", "Quality"],
        fill="toself",
    ))
    radar.update_layout(height=380, showlegend=False)
    st.plotly_chart(radar, use_container_width=True)

    st.markdown("## 🔎 Skill Gaps")
    st.dataframe(pd.DataFrame(skill_matrix), use_container_width=True)

    st.markdown("## 🧠 AI Resume Analysis")
    st.write(llm_analysis(resume_text, jd_text, api_key))

    st.markdown("## ✨ Improved Resume")
    improved = improve_resume(resume_text, jd_text, api_key)
    st.text_area("Improved Resume", improved, height=300)

    st.download_button("⬇ TXT", improved, "improved_resume.txt")
    st.download_button("⬇ PDF", export_pdf(improved), "improved_resume.pdf")
    st.download_button("⬇ DOCX", export_docx(improved), "improved_resume.docx")

# ============================
# CHAT
# ============================
st.markdown("## 💬 Chat with Resume")
if "resume_text" in st.session_state:
    q = st.text_input("Ask something about the resume")
    if q:
        st.success(chat_with_resume(st.session_state.resume_text, q, api_key))
else:
    st.info("Analyze a resume to chat with it.")
