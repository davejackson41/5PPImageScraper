import openai
import base64
import os
from config import OPENAI_API_KEY

# Define paths dynamically
ORIGINAL_IMAGE_PATH = "data/images/vaccination_cards/1713782940159.jpg"  # Change dynamically per image
IMAGE_NAME = os.path.basename(ORIGINAL_IMAGE_PATH)
PROCESSED_IMAGE_PATH = f"data/images/vaccination_cards/processed_{IMAGE_NAME}"

def encode_image(image_path):
    """Encodes an image as base64 for OpenAI processing."""
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

def extract_text_from_image(image_path):
    """Extracts text from the processed image using OpenAI's GPT-4 Vision."""
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"⚠️ Image not found: {image_path}")

    # Load and encode image
    image_base64 = encode_image(image_path)

    # Create OpenAI client
    client = openai.OpenAI(api_key=OPENAI_API_KEY)

    # OpenAI API request using GPT-4 Vision
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are an OCR assistant extracting text from a vaccination card image."},
            {"role": "user", "content": [
                {"type": "text", "text": "Extract all handwritten and printed text from this vaccination card."},
                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image_base64}"}}
            ]}
        ],
        max_tokens=500
    )

    # Extract and save the text
    extracted_text = response.choices[0].message.content

    output_path = f"data/extracted_text/extracted_{IMAGE_NAME.replace('.jpg', '')}.txt"
    with open(output_path, "w") as f:
        f.write(extracted_text)

    print(f"✅ OCR extraction complete. Text saved to: {output_path}")

    return extracted_text

# Run OCR processing
if __name__ == "__main__":
    extracted_text = extract_text_from_image(PROCESSED_IMAGE_PATH)
    print("\n🔹 Extracted Text:\n", extracted_text)