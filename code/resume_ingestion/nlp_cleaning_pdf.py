import spacy
import os
import unicodedata
nlp = spacy.load("en_core_web_sm")

def remove_unicode_noise(text):
    normalized = unicodedata.normalize("NFKD", text)
    return "".join(c for c in normalized if not unicodedata.combining(c))

def to_ascii(text):
    text = remove_unicode_noise(text)
    return "".join(c for c in text if ord(c) < 128)

def clean_text_spacy(text: str) -> str:
    text = to_ascii(text)
    doc = nlp(text)
    cleaned_sentences = []
    for sent in doc.sents:
        tokens = []
        for token in sent:
            if token.is_punct or token.is_space or token.is_stop:
                continue
            lemma = token.lemma_.strip().lower()
            if lemma:
                tokens.append(lemma)
        if tokens:
            cleaned_sentences.append(" ".join(tokens))
    return "\n".join(cleaned_sentences)


def save_to_text(cleaned_text: str, output_path: str):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(cleaned_text)

if __name__ == "__main__":
    input_file_path = r"D:\WORK\RMS\Project\code\my_data\nlp_extract.txt"
    output_file_path = r"D:\WORK\RMS\Project\code\my_data\nlp_clean.txt"

    with open(input_file_path, "r", encoding="utf-8") as f:
        raw_text = f.read()

    cleaned = clean_text_spacy(raw_text)
    save_to_text(cleaned, output_file_path)
    print(f"Cleaned text saved to: {output_file_path}")
