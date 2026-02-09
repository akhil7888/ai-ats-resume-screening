import streamlit as st

def render_header():
    st.markdown("<h1 style='text-align:center;'>AI ATS Resume Screening</h1>", unsafe_allow_html=True)


def render_upload_section():
    st.subheader("📂 Upload Your Resume")
    uploaded_file = st.file_uploader("Upload PDF or DOCX", type=["pdf", "docx"])

    st.subheader("📄 Job Description")
    jd = st.text_area("Paste the Job Description")

    return uploaded_file, jd


def render_ats_dashboard(scores, analysis, improved):
    st.subheader("📊 ATS Overview")

    col1, col2, col3 = st.columns(3)
    col1.metric("ATS Match", f"{scores['ats_match']}%")
    col2.metric("Job Fit", f"{scores['job_fit']}%")
    col3.metric("Resume Quality", f"{scores['resume_quality']}%")

    st.subheader("📘 ATS Analysis")
    st.write(analysis)

    st.subheader("✨ Improved Resume")
    st.write(improved)


def render_jd_generator_section():
    role = st.text_input("Enter job role")
    return role


def render_recruiter_section(resume):
    st.subheader("Recruiter Review")
    if resume:
        return st.button("Evaluate Resume")
    return False


def render_chat_section(resume):
    st.subheader("💬 Chat with Resume")
    return st.text_input("Ask something about the resume")
