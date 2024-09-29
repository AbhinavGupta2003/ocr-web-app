import pytesseract
from PIL import Image

# Path to Tesseract executable (if not in PATH, otherwise omit this line)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Function to extract text from an image using Tesseract
def extract_text_from_image(image_path):
    # Open the image using PIL
    image = Image.open(image_path)
    
    # Extract text from image using Tesseract
    extracted_text = pytesseract.image_to_string(image, lang='eng+hin')  # OCR for both English and Hindi
    
    return extracted_text
