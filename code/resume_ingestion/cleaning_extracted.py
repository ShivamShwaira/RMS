import re
import os

def clean_text(text):
    # Remove common header/footer patterns
    text = re.sub(r"Page \d+", "", text)
    text = re.sub(r"\d+/\d+", "", text)
    text = re.sub(r"Confidential.*", "", text)
    text = re.sub(r"Resume.*", "", text)
    text = re.sub(r"[-_=]{5,}.*", "", text)

    # Remove non-ASCII characters
    text = re.sub(r"[^a-zA-Z0-9.,;:!?'\n()\- ]", " ", text)

    # Normalize spaces and newlines
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"\n\s*\n+", "\n\n", text)

    return text.strip()


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
    input_folder =  "D:/WORK/RMS/Project/code/my_data/extracted_myresume"
    output_folder = "D:/WORK/RMS/Project/code/my_data/clean_myresume"

    clean_folder(input_folder, output_folder)
    print("Cleaning Complete")