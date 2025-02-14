import cv2
import pytesseract
import os
import logging
from PIL import Image

# Set up logging
LOG_FILE = "logs/gui_debug.log"
os.makedirs("logs", exist_ok=True)
logging.basicConfig(filename=LOG_FILE, level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")

IMAGE_DIR = "data/images/vaccination_cards/"
EXTRACTED_TEXT_DIR = "data/extracted_text/"

def preprocess_image(image_path):
    """Convert the image to grayscale, apply thresholding, and save a processed version."""
    try:
        logging.info(f"Processing image: {image_path}")
        img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        processed_path = os.path.join(IMAGE_DIR, f"processed_{os.path.basename(image_path)}")

        # Apply preprocessing
        img = cv2.GaussianBlur(img, (5, 5), 0)
        _, img = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)

        # Save processed image
        cv2.imwrite(processed_path, img)
        logging.info(f"Processed image saved: {processed_path}")
        return processed_path
    except Exception as e:
        logging.error(f"Error processing image: {e}")
        return None

def extract_text_from_image(image_path):
    """Run OCR on the processed image and return extracted text."""
    try:
        logging.info(f"Running OCR on image: {image_path}")
        img = Image.open(image_path)
        text = pytesseract.image_to_string(img)
        
        # Save extracted text
        extracted_text_path = os.path.join(EXTRACTED_TEXT_DIR, f"extracted_{os.path.basename(image_path)}.txt")
        with open(extracted_text_path, "w") as file:
            file.write(text)
        
        logging.info(f"OCR extraction complete. Text saved to: {extracted_text_path}")
        return extracted_text_path
    except Exception as e:
        logging.error(f"Error running OCR: {e}")
        return None