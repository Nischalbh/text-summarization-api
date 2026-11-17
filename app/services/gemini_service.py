import os
from dotenv import load_dotenv
from google import genai

# Load environment variables
load_dotenv()
# gemini API Key
api_key = os.getenv("GEMINI_API_KEY")
# Create gemini client
client = genai.Client(api_key=api_key)


def generate_summary(text: str, length: str, style: str):
    prompt = f"""
    Text Summarization assistant
    summary length: {length}
    Writing style: {style}
    original text: {text}
    Return only summary.
    """
    response = client.models.generate_content(model="gemini-3.8-flash", contents=prompt)
    return response.text
