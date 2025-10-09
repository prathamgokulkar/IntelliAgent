import fitz  
from src.agents import ocr_agent

# If direct extraction yields fewer characters than this, we'll trigger OCR.
MIN_TEXT_LENGTH_FOR_DIGITAL = 250

def load_pdf_text(pdf_path: str) -> str:
   
    print("Loader: Attempting direct text extraction...")
    text = ""
    try:
        with fitz.open(pdf_path) as doc:
            for page in doc:
                text += page.get_text()
        print("Loader: Direct extraction successful.")
    except Exception as e:
        print(f"--- Loader: Direct text extraction failed: {e} ---")
        text = ""

    if len(text.strip()) < MIN_TEXT_LENGTH_FOR_DIGITAL:
        print("Loader: Direct extraction yielded little text. Activating OCR Agent. ")
        text = ocr_agent.extract_text_from_scanned_pdf(pdf_path)

    if not text.strip():
        raise ValueError("Failed to extract any meaningful text from the PDF.")
    
    return text