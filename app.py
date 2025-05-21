import streamlit as st
import zipfile
import os
import shutil
import tempfile
from resume_utils import process_resumes

st.set_page_config(page_title="Bulk ATS Resume Formatter", layout="centered")

st.title("📂 Bulk ATS Resume Formatter")
st.markdown("""
Upload a ZIP file containing `.pdf` and `.docx` resumes (supports subfolders).  
The tool will extract them, convert each to ATS-friendly format, and let you download a new ZIP with formatted `.pdf` resumes.
""")

uploaded_zip = st.file_uploader("Upload ZIP of Resumes", type=["zip"])

if uploaded_zip:
    with tempfile.TemporaryDirectory() as temp_dir:
        raw_dir = os.path.join(temp_dir, "raw")
        os.makedirs(raw_dir, exist_ok=True)

        with zipfile.ZipFile(uploaded_zip, 'r') as zip_ref:
            zip_ref.extractall(raw_dir)

        ats_zip_path = os.path.join(temp_dir, "ats_resumes.zip")
        process_resumes(raw_dir, ats_zip_path)

        st.success("✅ All resumes formatted!")

        with open(ats_zip_path, "rb") as f:
            st.download_button(
                label="📥 Download ATS-Formatted ZIP",
                data=f.read(),
                file_name="ATS_Resumes.zip",
                mime="application/zip"
            )
