from fastapi import FastAPI
from app.models.schemas import SummarizeRequest, SummarizeResponse
from app.services.gemini_service import generate_summary

# Create Fast API Application
app = FastAPI(
    title="Text Summarization API",
    description="An AI-powered API that summarizes long text using Claude.",
)


# First endpoint
@app.get("/")
def home():
    return {
        "message": "Welcome to Text Summarization API",
        "status": "Running successfully",
    }


# health check endpoint
@app.get("/health")
def health_check():
    return {"status": "healthy", "application": "Text Summarization API"}


@app.post("/api/v1/summarize", response_model=SummarizeResponse)
def summarize(request: SummarizeRequest):
    return {
        "summary": "This is a sample summary.",
        "original_length": len(request.text),
        "summary_length": 27,
        "chunks_processed": 1,
        "style": request.style,
        "length": request.length,
    }
