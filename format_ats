def format_ats_resume(name, contact, summary, skills, experiences, education, certs, projects):
    def fallback(val, default):
        return val if val and (isinstance(val, list) and any(val) or isinstance(val, str) and val.strip()) else default

    return {
        "Name": name or "Candidate Name",
        "Contact": contact or "Phone | Email | LinkedIn | Location",
        "Summary": fallback(summary, "Motivated professional seeking impactful opportunities."),
        "Skills": fallback(skills, ["Time Management", "Teamwork", "Problem Solving"]),
        "Experience": fallback(experiences, ["Experience details available upon request."]),
        "Education": fallback(education, ["Education information not provided."]),
        "Certifications": fallback(certs, ["None listed."]),
        "Projects": fallback(projects, ["Project details not included."])
    }
