from app.models.schemas import SummarizeRequest, SummarizeResponse
from app.services.summarizer import summarize_long_text
from app.text_chunker import split_text_into_chunks
from fastapi import FastAPI, Depends, HTTPException, status
from google.genai import errors as genai_errors
from app.core.security import verify_api_key

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


@app.post(
    "/api/v1/summarize",
    response_model=SummarizeResponse,
    dependencies=[Depends(verify_api_key)],
)
def summarize(request: SummarizeRequest):
    # Split long text into chunks
    chunks = split_text_into_chunks(request.text)
    try:
        summary = summarize_long_text(
            text=request.text,
            length=request.length,
            style=request.style,
        )
    except genai_errors.APIError as exc:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"Summarization service is unavailable (upstream error {exc.code}).",
        ) from exc

    return {
        "summary": summary,
        "original_length": len(request.text),
        "summary_length": len(summary),
        "chunks_processed": len(chunks),
        "style": request.style,
        "length": request.length,
    }
