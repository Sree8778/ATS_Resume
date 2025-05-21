import streamlit as st
import zipfile
import os
import shutil
import tempfile
from resume_utils import process_resumes

st.set_page_config(page_title="Bulk ATS Resume Formatter", layout="centered")

st.title("📂 Bulk ATS Resume Formatter")

option = st.radio("Choose Upload Type:", ["Upload ZIP", "Upload Multiple Files/Folders"])

if option == "Upload ZIP":
    uploaded_zip = st.file_uploader("Upload ZIP of Resumes", type=["zip"])
elif option == "Upload Multiple Files/Folders":
    uploaded_files = st.file_uploader("Upload Individual Files or Folder", type=["pdf", "docx"], accept_multiple_files=True)

if (option == "Upload ZIP" and uploaded_zip) or (option == "Upload Multiple Files/Folders" and uploaded_files):
    with tempfile.TemporaryDirectory() as temp_dir:
        raw_dir = os.path.join(temp_dir, "raw")
        os.makedirs(raw_dir, exist_ok=True)

        if option == "Upload ZIP":
            with zipfile.ZipFile(uploaded_zip, 'r') as zip_ref:
                zip_ref.extractall(raw_dir)
        else:
            # Save each uploaded file into raw_dir
            for file in uploaded_files:
                file_path = os.path.join(raw_dir, file.name)
                with open(file_path, "wb") as f:
                    f.write(file.read())

        ats_zip_path = os.path.join(temp_dir, "ats_resumes.zip")
        process_resumes(raw_dir, ats_zip_path)

        st.success("✅ ATS Resumes generated successfully!")

        with open(ats_zip_path, "rb") as f:
            st.download_button(
                label="📥 Download ATS-Formatted ZIP",
                data=f.read(),
                file_name="ATS_Resumes.zip",
                mime="application/zip"
            )
