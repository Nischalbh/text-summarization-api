import os
from dotenv import load_dotenv
from google import genai

# Load environment variables
load_dotenv()
# gemini API Key
api_key = os.getenv("GEMINI_API_KEY")
# Create gemini client
client = genai.Client(api_key=api_key)
