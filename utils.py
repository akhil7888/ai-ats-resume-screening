import streamlit as st

# -------------------------------------
# Custom Dark UI
# -------------------------------------
def render_header():
    st.markdown(
        """
        <h1 style='text-align:center; color:#fff;'>📄 AI ATS Resume Screening</h1>
        <p style='text-align:center; color:#bbb;'>Powered by Groq — Fast • Accurate • Free</p>
        <hr style='border:1px solid #333;'/>
        """,
        unsafe_allow_html=True
    )

# Upload Section
def render_upload_section():
    st.subheader("📤 Upload Your Resume")
    file = st.file_uploader("Upload PDF or DOCX", type=["pdf", "docx"])

    st.subheader("📝 Job Description")
    jd = st.text_area("Paste Job Description")

    return file, jd

# Dashboard
def render_ats_dashboard(scores, analysis, improved):
    st.subheader("📊 ATS Overview")

    c1, c2, c3 = st.columns(3)
    c1.metric("Match", f"{scores['match']}%")
    c2.metric("Fit", f"{scores['fit']}%")
    c3.metric("Quality", f"{scores['quality']}%")

    st.subheader("📘 ATS Analysis")
    st.write(analysis)

    st.subheader("✨ Improved Resume")
    st.text_area("Improved Resume", improved, height=300)

# Chat Section
def render_chat_section(resume_text):
    st.subheader("💬 Chat with Resume")
    return st.text_input("Ask anything about the resume:")
