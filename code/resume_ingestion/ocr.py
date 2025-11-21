import os
from PIL import Image
import pytesseract
from pdf2image import convert_from_path
import shutil

# --- Configuration ---
INPUT_FOLDER = 'input_resumes'
OUTPUT_FOLDER = 'output_text_files'
# Optional Set the path to the Tesseract executable if needed (Windows example)
# pytesseract.pytesseract.tesseract_cmd = r'CProgram FilesTesseract-OCRtesseract.exe'
# Optional Set the path to the Poppler bin directory if needed (Windows example)
# POPPLER_PATH = r'Cpathtopoppler-xx.x.xLibrarybin' 
POPPLER_PATH = None # Set to None for LinuxmacOS or if Poppler is in system PATH

# --- Helper Functions from previous response ---

def extract_text_from_image(image_path)
    Extracts text from an image file using OCR.
    try
        img = Image.open(image_path)
        text = pytesseract.image_to_string(img)
        return text
    except Exception as e
        print(fError processing image {image_path} {e})
        return None

def extract_text_from_scanned_pdf(pdf_path, poppler_path=None)
    Converts a scanned PDF to images and performs OCR.
    all_text = 
    try
        # Pass poppler_path if specified, otherwise it uses system PATH
        images = convert_from_path(pdf_path, poppler_path=poppler_path)
        for image in images
            page_text = pytesseract.image_to_string(image)
            all_text += page_text + n
        return all_text
    except Exception as e
        print(fError processing PDF {pdf_path} {e})
        return None

# --- Main Processing Logic ---

def process_folder(input_dir, output_dir)
    # 1. Create the output folder if it doesn't exist
    if not os.path.exists(output_dir)
        os.makedirs(output_dir)
        print(fCreated output directory {output_dir})

    # 2. Iterate through all files in the input folder
    for filename in os.listdir(input_dir)
        input_path = os.path.join(input_dir, filename)
        
        # Skip directories
        if os.path.isdir(input_path)
            continue

        # Determine the output filename (change extension to .txt)
        base, ext = os.path.splitext(filename)
        output_filename = f{base}.txt
        output_path = os.path.join(output_dir, output_filename)

        extracted_text = None
        
        # 3. Process based on file extension
        if ext.lower() in ['.jpg', '.jpeg', '.png']
            print(fProcessing image file {filename})
            extracted_text = extract_text_from_image(input_path)
        elif ext.lower() == '.pdf'
            print(fProcessing PDF file {filename})
            extracted_text = extract_text_from_scanned_pdf(input_path, POPPLER_PATH)
        else
            print(fSkipping unsupported file type {filename})
            continue

        # 4. Save the extracted text to the output folder
        if extracted_text
            with open(output_path, 'w', encoding='utf-8') as f
                f.write(extracted_text)
            print(fSaved text to {output_filename})
        else
            print(fCould not extract text from {filename})

if __name__ == __main__
    # Ensure you have files in 'input_resumes' folder before running
    process_folder(INPUT_FOLDER, OUTPUT_FOLDER)
    print(nBatch processing complete.)
