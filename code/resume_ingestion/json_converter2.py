import json
import re
import os

def extract_name(text):
    lines = [l.strip() for l in text.split("\n") if l.strip()][:3]

    header = " ".join(lines)

    header = re.sub(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", " ", header)
    header = re.sub(r"\+?\d[\d\s\-()]{7,}", " ", header)
    header = re.sub(r"(https?://|www\.)\S+", " ", header)
    header = re.sub(r"\b(linkedin|github|portfolio|resume|cv|aspiring|developer|engineer|student)\b.*",
                    " ",
                    header,
                    flags=re.I)

    words = [w for w in header.split() if w.isalpha()]

    if len(words) >= 2:
        return f"{words[0]} {words[1]}"

    return ""

def extract_personal_info(text):
    email_pattern = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
    emails = re.findall(email_pattern, text)
    email = emails[0] if emails else ""
    # phone_pattern = r"(?:\+91[\s-]*)?(?:[6-9]\d{9})"
    # phone_pattern = r"(?:\+91[\s-]*)?(?:[6-9]\d{9})|(?:\d{3}[-.\s]\d{3}[-.\s]\d{4})"
    phone_pattern = r"""(?:
        (?:(?:Phone|Mob\.?|Mobile|Tel|Telephone|Cell)\s*[:\-]?\s*)   # Optional label
        )?
        (\+?\d{1,3}[\s\-\.]?)?       # Country code e.g. +1, +91
        \(?\d{2,4}\)?[\s\-\.]?       # Area code e.g. (847)
        \d{3,4}[\s\-\.]?\d{3,4}      # Main number 940-242-3303 or 2423303
    """
    phones = re.findall(phone_pattern, text)
    phone = phones[0] if phones else ""
    name = extract_name(text)
    return {"Name": name, "Email": email, "Phone": phone}




def load_skills_list(file_path="skills_list.txt"):
    with open(file_path, "r") as f:
        return [line.strip() for line in f if line.strip()]


def extract_skills(raw_section, skills_file="skills_list.txt"):
    skills_set = load_skills_list(skills_file)
    found = []

    lower_text = raw_section.lower()
    for skill in skills_set:
        if skill.lower() in lower_text:
            found.append(skill)

    return list(dict.fromkeys(found))



def resume_text_to_json(input_path, output_path):
    sections = [
        "OVERVIEW",
        "WORK EXPERIENCE",
        "EDUCATION",
        "PROJECTS",
        "SKILLS",
        "CERTIFICATIONS",
        "ACHIEVEMENTS"
    ]
    with open(input_path, "r", encoding="utf-8") as f:
        text = f.read()
    data = extract_personal_info(text)
    text_upper = text.upper()
    positions = {}
    for sec in sections:
        idx = text_upper.find(sec)
        if idx != -1:
            positions[sec] = idx
    sorted_sections = sorted(positions.items(), key=lambda x: x[1])
    for i in range(len(sorted_sections)):
        sec, start = sorted_sections[i]
        end = sorted_sections[i + 1][1] if (i + 1 < len(sorted_sections)) else len(text)
        content = text[start + len(sec):end].strip()
        content = re.sub(r"\s+", " ", content)
        data[sec.title()] = content
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

def process_resumes_folder(input_folder, output_folder):
    os.makedirs(output_folder, exist_ok=True)
    for file_name in os.listdir(input_folder):
        if file_name.lower().endswith(".txt"):
            input_file = os.path.join(input_folder, file_name)
            output_file = os.path.join(output_folder, os.path.splitext(file_name)[0] + ".json")
            resume_text_to_json(input_file, output_file)
    print("Processed all resumes.")

input_folder = r"D:/WORK/RMS/Project/code/my_data/clean_word"
output_folder = r"D:/WORK/RMS/Project/code/my_data/json_word"
skills_file = r"D:/WORK/RMS/Project/code/resume_ingestion/skills_list.txt"  

process_resumes_folder(input_folder, output_folder)