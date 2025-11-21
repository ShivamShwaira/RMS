import json
import re
import os

def resume_text_to_json(input_path, output_path):

    #defining sections
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


    text_upper = text.upper()


    positions = {}
    for s in sections:
        idx = text_upper.find(s)
        if idx != -1:
            positions[s] = idx

    sorted_sections = sorted(positions.items(), key=lambda x: x[1])

    data = {}


    for i in range(len(sorted_sections)):
        sec, start = sorted_sections[i]


        if i + 1 < len(sorted_sections):
            end = sorted_sections[i + 1][1]
        else:
            end = len(text)

        content = text[start + len(sec):end].strip()

    
        content = re.sub(r"\s+", " ", content)

        data[sec.title()] = content

    #json saving
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)




def process_resumes_folder(input_folder, output_folder):

    os.makedirs(output_folder, exist_ok=True)


    for file_name in os.listdir(input_folder):
        if file_name.lower().endswith(".txt"):

            input_file = os.path.join(input_folder, file_name)

            output_file = os.path.join(
                output_folder, 
                os.path.splitext(file_name)[0] + ".json"
            )

            resume_text_to_json(input_file, output_file)




input_folder = r"D:/WORK/RMS/Project/code/my_data/clean_myresume"
output_folder = r"D:/WORK/RMS/Project/code/my_data/json_myresume"

process_resumes_folder(input_folder, output_folder)
print("Processed")


# resume_text_to_json("D:/WORK/RMS/Project/code/my_data/clean_myresume/Shivam_Parab.txt", "D:/WORK/RMS/Project/code/my_data/json_myresume/Shivam_Parab.json")
