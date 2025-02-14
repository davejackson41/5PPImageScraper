import cv2
import numpy as np
import os

# Define paths
IMAGE_PATH = "data/images/vaccination_cards/1713782940159.jpg"  # Change this dynamically later if needed
IMAGE_NAME = os.path.basename(IMAGE_PATH)
OUTPUT_PATH = f"data/images/vaccination_cards/processed_{IMAGE_NAME}"

def preprocess_image(image_path, output_path):
    """Loads an image and applies improved preprocessing for OCR."""
    # Load image
    image = cv2.imread(image_path)

    if image is None:
        raise FileNotFoundError(f"⚠️ Image not found: {image_path}")

    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply histogram equalization for better contrast
    gray = cv2.equalizeHist(gray)

    # Apply bilateral filtering to reduce noise while keeping edges sharp
    filtered = cv2.bilateralFilter(gray, 9, 75, 75)

    # Use adaptive thresholding to enhance text contrast
    processed = cv2.adaptiveThreshold(
        filtered, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 15, 8
    )

    # Save preprocessed image
    cv2.imwrite(output_path, processed)
    print(f"✅ Preprocessed image saved: {output_path}")

    return output_path

# Run preprocessing
if __name__ == "__main__":
    preprocess_image(IMAGE_PATH, OUTPUT_PATH)