import os
from dotenv import load_dotenv
from google import genai

# Load environment variables
load_dotenv()

# gemini API Key
api_key = os.getenv("GEMINI_API_KEY")

# Model can be overridden from .env; the default is a currently available model.
model_name = os.getenv("GEMINI_MODEL", "gemini-3.1-flash-lite")

# Create gemini client with a timeout so a slow/unavailable model cannot hang the API.
client = genai.Client(api_key=api_key, http_options={"timeout": 20000})


def generate_summary(text: str, length: str, style: str):
    prompt = f"""
    Text Summarization assistant
    summary length: {length}
    Writing style: {style}
    original text: {text}
    Return only summary.
    """
    response = client.models.generate_content(model=model_name, contents=prompt)
    return response.text
