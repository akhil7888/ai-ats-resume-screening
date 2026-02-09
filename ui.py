import streamlit as st


# ---------------------------
# HEADER
# ---------------------------
def render_header():
    st.markdown(
        "<h1 style='text-align:center;'>📄 AI ATS Resume Screening</h1>",
        unsafe_allow_html=True,
    )
    st.markdown(
        "<p style='text-align:center;'>Powered by Groq • Fast • Accurate • Free</p>",
        unsafe_allow_html=True,
    )
    st.write("---")


# ---------------------------
# UPLOAD SECTION
# ---------------------------
def render_upload_section():
    st.subheader("📤 Upload Your Resume")
    resume_file = st.file_uploader("Upload resume (PDF / DOCX)", type=["pdf", "docx"])

    st.subheader("📝 Job Description")
    jd_text = st.text_area("Paste the job description here")

    return resume_file, jd_text


# ---------------------------
# ATS DASHBOARD
# ---------------------------
def render_ats_dashboard(scores, analysis, improved):
    st.subheader("📊 ATS Overview")

    c1, c2, c3 = st.columns(3)
    c1.metric("ATS Match", f"{scores['match']}%")
    c2.metric("Job Fit", f"{scores['fit']}%")
    c3.metric("Resume Quality", f"{scores['quality']}%")

    st.subheader("🧠 ATS Analysis")
    st.write(analysis)

    st.subheader("✨ Improved Resume")
    st.text_area("Improved Resume", improved, height=300)


# ---------------------------
# JD GENERATOR
# ---------------------------
def render_jd_generator():
    st.subheader("📝 Job Description Generator")
    role = st.text_input("Enter Job Role")

    if st.button("Generate JD"):
        return role
    return None


# ---------------------------
# RECRUITER MODE
# ---------------------------
def render_recruiter_mode():
    st.subheader("🧑‍💼 Recruiter Evaluation Mode")
    st.write("Click below to evaluate the uploaded resume:")
    return st.button("Evaluate Resume")


# ---------------------------
# CHAT SECTION
# ---------------------------
def render_chat_section(resume_text):
    st.subheader("💬 Chat with Resume")
    st.write("Ask anything about the uploaded resume:")
    return st.text_input("Your Question")
