import pytesseract
from pdf2image import convert_from_path

def extract_text_from_scanned_pdf(pdf_path: str) -> str:
    
    print(f"--- OCR Agent: Starting OCR process for {pdf_path} ---")
    try:
        images = convert_from_path(pdf_path)
        
        full_text = ""
        
        for i, image in enumerate(images):
            print(f"--- OCR Agent: Processing page {i + 1}/{len(images)} ---")
            text = pytesseract.image_to_string(image)
            full_text += text + "\n\n"
        print(f"--- OCR Agent: OCR process completed successfully for {pdf_path} ---")
        return full_text
        
    except Exception as e:
        print(f"!!!!!! ERROR in OCR Agent for {pdf_path}: {e} !!!!!!")
        return ""

