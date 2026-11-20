from fastapi import FastAPI
from app.models.schemas import SummarizeRequest, SummarizeResponse
from app.services.gemini_service import generate_summary
from app.text_chunker import split_text_into_chunks

# Create Fast API Application
app = FastAPI(
    title="Text Summarization API",
    description="An AI-powered API that summarizes long text using Gemini.",
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
    # Split long text into chunks, summarize each, then combine the results.
    chunks = split_text_into_chunks(request.text)
    summaries = [
        generate_summary(
            text=chunk,
            length=request.length,
            style=request.style,
        )
        for chunk in chunks
    ]
    summary = "\n\n".join(summaries)

    return {
        "summary": summary,
        "original_length": len(request.text),
        "summary_length": len(summary),
        "chunks_processed": len(chunks),
        "style": request.style,
        "length": request.length,
    }
