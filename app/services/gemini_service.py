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

LENGTH_INSTRUCTIONS = {
    "short": "Write a concise summary in 2-3 sentences.",
    "medium": "Write a balanced summary in 1-2 paragraphs.",
    "long": "Write a detailed summary covering all important information.",
}

STYLE_INSTRUCTIONS = {
    "professional": "Use a clear, formal and professional tone.",
    "casual": "Use friendly, simple and conversational language.",
    "academic": "Use formal academic language and objective explanations.",
    "bullet_points": "Present the summary as clear and organized bullet points.",
}


def generate_summary(text: str, length: str, style: str):
    prompt = f"""
    expert text summarization assistant.

    TASK:
    Summarize the provided text.

    LENGTH:
    {LENGTH_INSTRUCTIONS[length]}

    STYLE:
    {STYLE_INSTRUCTIONS[style]}

    IMPORTANT RULES:
    - Keep the original meaning.
    - Do not invent facts.
    - Include the most important information.
    - Avoid unnecessary repetition.
    - Return only the summary.

    ORIGINAL TEXT:
    {text}
    """
    response = client.models.generate_content(model=model_name, contents=prompt)
    return response.text


def combine_summaries(summaries: list[str], length: str, style: str):
    """Merge partial chunk summaries into one coherent final summary."""
    numbered_summaries = "\n".join(
        f"{index}. {summary}" for index, summary in enumerate(summaries, start=1)
    )
    prompt = f"""
    expert text summarization assistant.

    TASK:
    Combine the following partial summaries into ONE coherent final summary.

    LENGTH:
    {LENGTH_INSTRUCTIONS[length]}

    STYLE:
    {STYLE_INSTRUCTIONS[style]}

    IMPORTANT RULES:
    - Merge all key points into a single unified summary.
    - Do not repeat the same information.
    - Do not invent facts.
    - Return only the final summary.

    PARTIAL SUMMARIES:
    {numbered_summaries}
    """
    response = client.models.generate_content(model=model_name, contents=prompt)
    return response.text
