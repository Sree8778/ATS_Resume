import streamlit as st
import tempfile
import os
from extract_text import extract_text_from_docx, extract_text_from_pdf
from format_ats import format_ats_resume
from export_pdf import export_ats_to_pdf

st.set_page_config(page_title="ATS Resume Builder", layout="centered")
st.title("📄 ATS Resume Builder")

choice = st.radio("Choose Input Method", ["Upload Existing Resume", "Create New Resume from Scratch"])

if choice == "Upload Existing Resume":
    uploaded_file = st.file_uploader("Upload your resume (.docx or .pdf)", type=["docx", "pdf"])

    if uploaded_file:
        file_ext = uploaded_file.name.split(".")[-1]
        with tempfile.NamedTemporaryFile(delete=False, suffix=f".{file_ext}") as temp:
            temp.write(uploaded_file.read())
            temp_path = temp.name

        if file_ext == "docx":
            raw_text = extract_text_from_docx(temp_path)
        else:
            raw_text = extract_text_from_pdf(temp_path)

        st.text_area("Extracted Text", raw_text, height=300)

        st.warning("🛠 Manual editing and structuring not implemented in this upload mode yet. Use 'Create New Resume' for perfect structure.")

elif choice == "Create New Resume from Scratch":
    st.header("📝 Create Your ATS Resume")

    with st.form("resume_form"):
        name = st.text_input("Full Name")
        contact = st.text_input("Contact (Phone | Email | LinkedIn | Location)")
        summary = st.text_area("Professional Summary", height=100)
        skills = st.text_area("Skills (comma-separated)")

        st.subheader("Experience")
        job_title = st.text_input("Job Title")
        company = st.text_input("Company")
        duration = st.text_input("Duration")
        job_desc = st.text_area("Job Description (each bullet on a new line)", height=100)

        st.subheader("Education")
        education = st.text_area("Education", height=80)

        st.subheader("Certifications")
        certs = st.text_area("Certifications (one per line)", height=60)

        st.subheader("Projects")
        projects = st.text_area("Projects (one per line)", height=80)

        submitted = st.form_submit_button("Generate ATS Resume")

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
            st.success("✅ Your resume has been created!")
            st.download_button(
                label="📥 Download ATS Resume",
                data=f.read(),
                file_name=f"{name.replace(' ', '_')}_ATS_Resume.pdf",
                mime="application/pdf"
            )
