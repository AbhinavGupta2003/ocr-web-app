import streamlit as st
from PIL import Image
import pytesseract
import cv2
import numpy as np

# Set up pytesseract path for Windows (uncomment this if needed)
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Custom CSS to style the app
st.markdown("""
    <style>
    .title {
        font-size: 2.5rem;
        color: #3498db;
        text-align: center;
        margin-top: -50px;
    }
    .caption {
        font-size: 1.1rem;
        color: #7f8c8d;
    }
    .stButton>button {
        background-color: #2ecc71;
        color: white;
        border-radius: 8px;
    }
    .highlight {
        background-color: #cce5ff;
        color: black;
        padding: 2px;
        border-radius: 3px;
    }
    .search-box {
        font-size: 1.2rem;
        padding: 10px;
        border: 2px solid #2ecc71;
        border-radius: 5px;
    }
    .found-text {
        color: #2ecc71;         
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

# Title section
st.markdown('<h1 class="title">OCR Web Application</h1>', unsafe_allow_html=True)
st.write("### Upload an image and extract text in both English and Hindi!")

# Preprocessing function for better OCR accuracy (optional)
def preprocess_image(image):
    # Convert to grayscale
    image = np.array(image)
    gray_image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    
    # Apply thresholding to enhance contrast (can improve OCR accuracy)
    _, thresh_image = cv2.threshold(gray_image, 150, 255, cv2.THRESH_BINARY)
    
    return Image.fromarray(thresh_image)

# File uploader for images
uploaded_file = st.file_uploader("Upload an image (PNG, JPG, JPEG)", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    # Display the uploaded image
    image = Image.open(uploaded_file)
    st.image(image, caption='Uploaded Image', use_column_width=True)
    
    # Optional: Apply preprocessing to enhance OCR accuracy
    preprocessed_image = preprocess_image(image)

    # Perform OCR using pytesseract
    with st.spinner("Extracting text..."):
        try:
            # Ensure pytesseract is using both English and Hindi language models
            ocr_text = pytesseract.image_to_string(preprocessed_image, lang="eng+hin")  # Support for both English and Hindi

            if not ocr_text.strip():
                st.warning("No text could be extracted. Try a clearer image.")
            else:
                st.subheader("Extracted Text")
                st.write(f'<p class="caption">{ocr_text}</p>', unsafe_allow_html=True)

        except pytesseract.TesseractError as e:
            st.error(f"OCR failed: {e}")

    # Keyword search functionality
    st.subheader("Keyword Search")
    search_query = st.text_input("Enter a keyword to search in the extracted text", placeholder="Type your keyword...")

    if search_query:
        # Search for the keyword in the extracted text (case-insensitive)
        if search_query.lower() in ocr_text.lower():
            st.markdown(f"<p class='found-text'>'{search_query}' found in the extracted text!</p>", unsafe_allow_html=True)
            # Highlight the found text in light blue
            highlighted_text = ocr_text.replace(search_query, f"<span class='highlight'>{search_query}</span>")
            st.markdown(f"<p>{highlighted_text}</p>", unsafe_allow_html=True)
        else:
            st.error(f"'{search_query}' not found.")

# Footer for better user experience
st.markdown("""
    <hr>
    <p style="text-align:center;">Developed by <strong>Abhinav Gupta</strong> | © 2024</p>
""", unsafe_allow_html=True)
