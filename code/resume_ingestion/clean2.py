import re
import os


def extract_emails(text):
    pattern = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
    return re.findall(pattern, text)


def clean_text(text):
    
    emails = extract_emails(text)

    # Replace each email with a placeholder
    for i, email in enumerate(emails):
        text = text.replace(email, f"__EMAIL_{i}__")

    text = re.sub(r"Page \d+", "", text)
    text = re.sub(r"\d+/\d+", "", text)
    text = re.sub(r"Confidential.*", "", text)
    text = re.sub(r"Resume.*", "", text)
    text = re.sub(r"[-_=]{5,}.*", "", text)

    # @ and _ for emaisl
    text = re.sub(r"[^a-zA-Z0-9@_.,;:!?'\n()\- ]", " ", text)

    # Normalize spaces
    text = re.sub(r"\s+", " ", text).strip()

    for i, email in enumerate(emails):
        text = text.replace(f"__EMAIL_{i}__", email)

    return text


def clean_folder(input_folder, output_folder):
    os.makedirs(output_folder, exist_ok=True)

    for filename in os.listdir(input_folder):
        if filename.endswith(".txt"):
            with open(os.path.join(input_folder, filename), "r", encoding="utf-8", errors="ignore") as f:
                raw = f.read()

            cleaned = clean_text(raw)

            with open(os.path.join(output_folder, filename), "w", encoding="utf-8") as f:
                f.write(cleaned)


if __name__ == "__main__":
    input_folder = "D:/WORK/RMS/Project/dataset/all_data/extracted_word"
    output_folder = "D:/WORK/RMS/Project/code/my_data/clean_word"

    clean_folder(input_folder, output_folder)
    print("Cleaning Complete")
