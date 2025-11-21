import json
from docxtpl import DocxTemplate


def split_points(text):
    if not text:
        return []
    text = str(text)
    for sep in [". ", "; ", "\n", "•"]:
        text = text.replace(sep, "|")
    return [p.strip() for p in text.split("|") if p.strip()]



def normalize_education(education_raw):
    EDUCATION = []

    if not education_raw:
        return EDUCATION

    if isinstance(education_raw, str):
        parts = [p.strip() for p in education_raw.split("||")]
        EDUCATION.append({
            "degree": parts[0] if len(parts) > 0 else "",
            "year": parts[1] if len(parts) > 1 else "",
            "college": parts[2] if len(parts) > 2 else ""
        })
        return EDUCATION

    if isinstance(education_raw, list):
        for edu in education_raw:
            if isinstance(edu, dict):
                EDUCATION.append({
                    "degree": edu.get("degree", ""),
                    "year": edu.get("year", ""),
                    "college": edu.get("college", "")
                })
            elif isinstance(edu, str):
                parts = [p.strip() for p in edu.split("||")]
                EDUCATION.append({
                    "degree": parts[0] if len(parts) > 0 else "",
                    "year": parts[1] if len(parts) > 1 else "",
                    "college": parts[2] if len(parts) > 2 else ""
                })
    return EDUCATION



def normalize_experience(experience_raw):
    EXPERIENCE = []

    if not experience_raw:
        return EXPERIENCE

    if isinstance(experience_raw, str):
        EXPERIENCE.append({
            "designation": "",
            "company": "",
            "duration": "",
            "points": split_points(experience_raw)
        })
        return EXPERIENCE

    if isinstance(experience_raw, list):
        for exp in experience_raw:
            if isinstance(exp, dict):
                EXPERIENCE.append({
                    "designation": exp.get("designation", ""),
                    "company": exp.get("company", ""),
                    "duration": exp.get("duration", ""),
                    "points": split_points(exp.get("points", []))
                })
            elif isinstance(exp, str):
                EXPERIENCE.append({
                    "designation": "",
                    "company": "",
                    "duration": "",
                    "points": split_points(exp)
                })

    return EXPERIENCE



def normalize_projects(projects_raw):
    PROJECTS = []

    if not projects_raw:
        return PROJECTS

    if isinstance(projects_raw, list):
        for p in projects_raw:
            if isinstance(p, dict):
                PROJECTS.append({
                    "name": p.get("name", ""),
                    "description": split_points(" ".join(p.get("description", [])))
                })
            elif isinstance(p, str):
                PROJECTS.append({"name": p, "description": []})

    return PROJECTS



def fill_resume_from_json(template_path, json_path, output_path):
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    doc = DocxTemplate(template_path)

    name = data.get("Name", "")
    summary = data.get("Overview", "")

    # TECHNOLOGIES block
    def to_list(val):
        if isinstance(val, list):
            return val
        if isinstance(val, str):
            return split_points(val)
        return []

    technologies = {
        "Languages": to_list(data.get("Technologies", {}).get("Languages", [])),
        "Backend": to_list(data.get("Technologies", {}).get("Backend", [])),
        "Cloud": to_list(data.get("Technologies", {}).get("Cloud", [])),
        "Databases": to_list(data.get("Technologies", {}).get("Databases", [])),
        "DevOps": to_list(data.get("Technologies", {}).get("DevOps", [])),
        "Tools": to_list(data.get("Technologies", {}).get("Tools", []))
    }

    EXPERIENCE = normalize_experience(data.get("Experience", []))
    EDUCATION = normalize_education(data.get("Education", []))
    PROJECTS = normalize_projects(data.get("Projects", []))
    CERTIFICATIONS = data.get("Certifications", [])
    ACHIEVEMENTS = data.get("Achievements", [])

    context = {
        "NAME": name,
        "SUMMARY": summary,
        "TECHNOLOGIES": technologies,
        "EXPERIENCE": EXPERIENCE,
        "EDUCATION": EDUCATION,
        "PROJECTS": PROJECTS,
        "CERTIFICATIONS": CERTIFICATIONS,
        "ACHIEVEMENTS": ACHIEVEMENTS
    }

    doc.render(context)
    doc.save(output_path)
    print("✔ Resume generated at:", output_path)


fill_resume_from_json(
    template_path="D:/WORK/RMS/Project/code/company_template_with_placeholders.docx",  # your uploaded template
    json_path="D:/WORK/RMS/Project/code/my_data/json_myresume2/Shivam_Parab.json",                    # your JSON file
    output_path="D:\WORK\RMS\exported_resumes\Final_Resume4.docx"              # output file
)
