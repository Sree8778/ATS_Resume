import streamlit as st
import tempfile
import os

from extract_text import extract_text_from_docx, extract_text_from_pdf
from format_ats import format_ats_resume
from export_pdf import export_ats_to_pdf
from chathcp_api import extract_ats_fields_from_text

st.set_page_config(page_title="Smart ATS Resume Builder", layout="centered")
st.title("📄 AI-Powered ATS Resume Builder")

choice = st.radio("Choose an Option", ["Upload Resume", "Create New Resume from Scratch"])

# ---- Upload Mode ----
if choice == "Upload Resume":
    uploaded_file = st.file_uploader("Upload a .docx or .pdf resume", type=["docx", "pdf"])

    if uploaded_file:
        file_ext = uploaded_file.name.split(".")[-1]
        with tempfile.NamedTemporaryFile(delete=False, suffix=f".{file_ext}") as temp:
            temp.write(uploaded_file.read())
            file_path = temp.name

        st.info("📥 Resume uploaded. Extracting content...")

        raw_text = extract_text_from_docx(file_path) if file_ext == "docx" else extract_text_from_pdf(file_path)
        st.text_area("🧾 Extracted Resume Text", raw_text, height=300)

        if st.button("🤖 Use ChatHCP to Auto-Format"):
            ats_resume = extract_ats_fields_from_text(raw_text)

            output_path = os.path.join(tempfile.gettempdir(), "ATS_Resume_AI.pdf")
            export_ats_to_pdf(ats_resume, output_path)

            with open(output_path, "rb") as f:
                st.success("✅ ATS resume created using ChatHCP!")
                st.download_button("📥 Download ATS Resume (PDF)", f.read(), "ATS_Resume.pdf", mime="application/pdf")

# ---- Manual Form Mode ----
elif choice == "Create New Resume from Scratch":
    st.header("📝 Build Your ATS Resume")

    with st.form("resume_form"):
        name = st.text_input("Full Name")
        contact = st.text_input("Contact (Phone | Email | LinkedIn | Location)")
        summary = st.text_area("Professional Summary", height=100)
        skills = st.text_area("Skills (comma-separated)")
        job_title = st.text_input("Job Title")
        company = st.text_input("Company")
        duration = st.text_input("Duration")
        job_desc = st.text_area("Job Description (bullet points per line)", height=100)
        education = st.text_area("Education Details", height=80)
        certs = st.text_area("Certifications (one per line)", height=60)
        projects = st.text_area("Projects (one per line)", height=80)
        submitted = st.form_submit_button("🎯 Generate ATS Resume")

    if submitted:
        resume_data = format_ats_resume(
            name=name,
            contact=contact,
            summary=summary,
            skills=[s.strip() for s in skills.split(",") if s.strip()],
            experiences=[f"{job_title} – {company} – {duration}", job_desc],
            education=[education],
            certs=[c.strip() for c in certs.splitlines() if c.strip()],
            projects=[p.strip() for p in projects.splitlines() if p.strip()]
        )

        output_path = os.path.join(tempfile.gettempdir(), f"{name.replace(' ', '_')}_ATS.pdf")
        export_ats_to_pdf(resume_data, output_path)

        with open(output_path, "rb") as f:
            st.success("✅ ATS Resume created!")
            st.download_button("📥 Download ATS Resume (PDF)", f.read(), f"{name.replace(' ', '_')}_ATS.pdf", mime="application/pdf")
