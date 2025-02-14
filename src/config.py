import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Retrieve the OpenAI API key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Validate that the API key is loaded
if not OPENAI_API_KEY:
    raise ValueError("⚠️ OpenAI API Key is missing! Make sure to set it in the .env file.")