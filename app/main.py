from fastapi import FastAPI
from app.models.schemas import SummarizeRequest, SummarizeResponse

# Create Fast API Application
app = FastAPI(
    title="Text Summarization API",
    description="An AI-powered API that summarizes long text.",
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
        "summary": "AI-generated summary will appear here.",
        "original_length": len(request.text),
        "summary_length": 100,
        "chunks_processed": 1,
        "style": request.style,
        "length": request.length,
    }
