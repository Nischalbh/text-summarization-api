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
    # Define summary
    length_instructions = {
        "short": "Write a concise summary in 2-3 sentences.",
        "medium": "Write a balanced summary in 1-2 paragraphs.",
        "long": "Write a detailed summary covering all important information.",
    }

    # Define writing
    style_instructions = {
        "professional": "Use a clear, formal and professional tone.",
        "casual": "Use friendly, simple and conversational language.",
        "academic": "Use formal academic language and objective explanations.",
        "bullet_points": "Present the summary as clear and organized bullet points.",
    }

    # Get instruction
    selected_length = length_instructions[length]
    selected_style = style_instructions[style]

    # Create prompt
    prompt = f"""
    expert text summarization assistant.

    TASK:
    Summarize the provided text.

    LENGTH:
    {selected_length}

    STYLE:
    {selected_style}

    IMPORTANT RULES:
    - Keep the original meaning.
    - Do not invent facts.
    - Include the most important information.
    - Avoid unnecessary repetition.
    - Return only the summary.

    ORIGINAL TEXT:
    {text}
    """

    # Send request
    response = client.models.generate_content(model=model_name, contents=prompt)

    return response.text
