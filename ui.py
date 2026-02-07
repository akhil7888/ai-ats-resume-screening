import streamlit as st

# -----------------------------
# HEADER
# -----------------------------
def render_header():
    st.markdown("""
        <div class='glass-header'>
            <h1>📄 AI ATS Resume Screening</h1>
            <p>Powered by Groq • Fast • Accurate • Free</p>
        </div>
    """, unsafe_allow_html=True)


# -----------------------------
# UPLOAD SECTION
# -----------------------------
def render_upload_section():
    st.subheader("📤 Upload Your Resume")
    resume_file = st.file_uploader("Upload resume (PDF / DOCX)", type=["pdf", "docx"])

    st.subheader("📝 Job Description")
    jd_text = st.text_area("Paste the job description here")

    return resume_file, jd_text


# -----------------------------
# ATS DASHBOARD
# -----------------------------
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


# -----------------------------
# JD GENERATOR
# -----------------------------
def render_jd_generator():
    st.subheader("📝 Job Description Generator")

    role = st.text_input("Enter job role")

    if st.button("Generate JD"):
        st.session_state["generated_jd"] = role


# -----------------------------
# RECRUITER MODE
# -----------------------------
def render_recruiter_mode():
    st.subheader("🧑‍💼 Recruiter Mode")

    resume_text = st.session_state.get("resume_text", "")

    if resume_text:
        st.write("Resume loaded.")
    else:
        st.warning("Upload resume in ATS Scanner first!")

    return resume_text


# -----------------------------
# CHAT SECTION
# -----------------------------
def render_chat_section(resume_text):
    st.subheader("💬 Chat with Resume")

    question = st.text_input("Ask something about the resume")
    return question
