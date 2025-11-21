import re
import os


HEADER_FOOTER_PAT = re.compile(r"(^Page \d+ of \d+)|(^\s*Page \d+\s*$)", re.IGNORECASE | re.MULTILINE)
PAGE_NUMBER_PAT = re.compile(r"\n?\s*\d+\s*\n")
MULTISPACE = re.compile(r"[ \t]{2,}")
SYMBOLS = re.compile(r"[•■▪▶★✦–—]+")

def clean_text(text):

    text = HEADER_FOOTER_PAT.sub("", text)
    text = PAGE_NUMBER_PAT.sub("\n", text)
    text = re.sub(r"\bConfidential.*", "", text, flags=re.IGNORECASE)
    text = re.sub(r"\bResume.*", "", text, flags=re.IGNORECASE)
    text = re.sub(r"[-_=]{5,}", "", text)
    text = SYMBOLS.sub("•", text)    
    text = re.sub(r"[^a-zA-Z0-9.,;:!?'\n()\- ]", " ", text)
    text = MULTISPACE.sub(" ", text)          
    text = re.sub(r"\s+\n", "\n", text)       
    text = re.sub(r"\n{3,}", "\n\n", text)     
    text = re.sub(r"[ ]{2,}", " ", text)    

    return text.strip()


def clean_folder(input_folder, output_folder):
    os.makedirs(output_folder, exist_ok=True)

    for filename in os.listdir(input_folder):
        if filename.endswith(".txt"):
            path = os.path.join(input_folder, filename)

            with open(path, "r", encoding="utf-8", errors="ignore") as f:
                raw = f.read()

            cleaned = clean_text(raw)

            with open(os.path.join(output_folder, filename), "w", encoding="utf-8") as f:
                f.write(cleaned)



if __name__ == "__main__":
    input_folder =  "D:/WORK/RMS/Project/code/my_data/extracted_myresume"
    output_folder = "D:/WORK/RMS/Project/code/my_data/clean_myresume"

    clean_folder(input_folder, output_folder)
    print("Cleaning Complete")