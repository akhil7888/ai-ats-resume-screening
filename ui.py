import streamlit as st

# HEADER
def render_header():
    st.markdown("<h1 style='text-align:center;'>📄 AI ATS Resume Screening</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center;'>Powered by Groq • Fast • Accurate • Free</p>", unsafe_allow_html=True)
    st.write("---")

# UPLOAD SECTION
def render_upload_section():
    st.subheader("📤 Upload Your Resume")
    resume_file = st.file_uploader("Upload resume (PDF / DOCX)", type=["pdf", "docx"])

    st.subheader("📝 Job Description")
    jd_text = st.text_area("Paste the job description here")

    return resume_file, jd_text

# ATS DASHBOARD
def render_ats_dashboard(scores, analysis, improved):
    st.subheader("📊 ATS Overview")

    col1, col2, col3 = st.columns(3)
    col1.metric("ATS Match", f"{scores['match']}%")
    col2.metric("Job Fit", f"{scores['fit']}%")
    col3.metric("Resume Quality", f"{scores['quality']}%")

    st.subheader("📘 ATS Analysis")
    st.write(analysis)

    st.subheader("✨ Improved Resume")
    st.text_area("Improved Resume", improved, height=300)

# JD GENERATOR
def render_jd_generator():
    st.subheader("📝 Job Description Generator")
    st.info("Enter a role on the left to generate.")

# RECRUITER MODE
def render_recruiter_mode():
    st.subheader("🧑‍💼 Recruiter Mode")
    st.info("Upload a resume first in ATS Scanner.")

# CHAT SECTION
def render_chat_section():
    st.subheader("💬 Chat with Resume")
    return st.text_input("Ask something about the resume")
