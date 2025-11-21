import pymupdf
import os

def extract_text_from_pdf(path: str) -> str:
    doc = pymupdf.open(path)
    text = ""

    for page in doc:
        text += page.get_text()

    doc.close()
    return text


# # individual text files

# def extract_from_folder(input_folder: str, output_file: str):
#     all_files = os.listdir(input_folder)

#     with open(output_file, "w", encoding="utf-8") as new_file:
#         for file_name in all_files:
#             if file_name.endswith(".pdf"):
#                 pdf_path = os.path.join(input_folder, file_name)

#                 text = extract_text_from_pdf(pdf_path)

#                 new_file.write(f"===== PROFILE: {file_name} =====\n")
#                 new_file.write(text)
#                 new_file.write("\n\n")





# separate tecxt files

def extract_from_folder(input_folder: str, output_folder: str):
    os.makedirs(output_folder, exist_ok=True)

    files = os.listdir(input_folder)

    for file_name in files:
        if file_name.endswith(".pdf"):
            pdf_path = os.path.join(input_folder, file_name)

            text = extract_text_from_pdf(pdf_path)

            txt_name = file_name.replace(".pdf", ".txt")
            txt_path = os.path.join(output_folder, txt_name)

            with open(txt_path, "w", encoding="utf-8") as new_file:
                new_file.write(text)

            # print(f"Created: {txt_path}")



    
if __name__ == "__main__":
    input_folder = "D:/WORK/RMS/Project/code/my_data/my_resume"
    output_folder = "D:/WORK/RMS/Project/code/my_data/extracted_myresume"

    extract_from_folder(input_folder, output_folder)
    print("Extraction Complete")