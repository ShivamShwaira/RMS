import pymupdf  # PyMuPDF
import spacy
import os

# Load spaCy model
nlp = spacy.load("en_core_web_sm")


def extract_text_pymupdf(pdf_path):
    """Extract raw text from a PDF using PyMuPDF."""
    doc = pymupdf.open(pdf_path)
    full_text = []

    for page in doc:
        text = page.get_text("text")
        if text.strip():
            full_text.append(text)

    doc.close()
    return "\n".join(full_text)


def clean_with_spacy(text):
    """
    Clean text using ONLY spaCy NLP — no regex.
    """
    doc = nlp(text)
    cleaned_sentences = []

    for sent in doc.sents:
        tokens = []
        for token in sent:
            # Skip punctuation, spaces, stopwords
            if token.is_punct or token.is_space or token.is_stop:
                continue

            # Add lemmatized lowercase token
            lemma = token.lemma_.strip().lower()
            if lemma:
                tokens.append(lemma)

        if tokens:
            cleaned_sentences.append(" ".join(tokens))

    return "\n".join(cleaned_sentences)


def save_cleaned_text(text, output_path):
    """Save cleaned text to a .txt file."""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(text)


def extract_clean_and_save(pdf_path, output_txt_file):
    """Complete pipeline."""
    raw_text = extract_text_pymupdf(pdf_path)
    cleaned_text = clean_with_spacy(raw_text)
    save_cleaned_text(cleaned_text, output_txt_file)
    print(f"Cleaned text saved to: {output_txt_file}")



def clean_text_spacy(text: str) -> str:

    doc = nlp(text)
    cleaned_sentences = []

    for sent in doc.sents:
        tokens = []

        for token in sent:
            # Skip unnecessary tokens
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


# Example usage
if __name__ == "__main__":
    pdf_file = r"D:\WORK\RMS\Project\code\my_data\my_resume\Shivam_Parab.pdf"
    output_text_file = r"D:\WORK\RMS\Project\code\my_data\nlp_extract.txt"

    extract_clean_and_save(pdf_file, output_text_file)
