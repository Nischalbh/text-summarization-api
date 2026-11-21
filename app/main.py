from fastapi import FastAPI, Depends, HTTPException, status
from google.genai import errors as genai_errors

from app.models.schemas import SummarizeRequest, SummarizeResponse
from app.services.summarizer import summarize_long_text
from app.text_chunker import split_text_into_chunks
from app.core.rate_limiter import rate_limit
from app.core.logger import logger

# Create FastAPI application
app = FastAPI(
    title="Text Summarization API",
    description="An AI-powered API that summarizes long text using Gemini.",
)


# Home endpoint
@app.get("/")
def home():
    logger.info("Home endpoint accessed")

    return {
        "message": "Welcome to Text Summarization API",
        "status": "Running successfully",
    }


# Health check endpoint
@app.get("/health")
def health_check():
    logger.info("Health check endpoint accessed")

    return {
        "status": "healthy",
        "application": "Text Summarization API",
    }


# Summarization endpoint
@app.post(
    "/api/v1/summarize",
    response_model=SummarizeResponse,
    dependencies=[Depends(rate_limit)],
)
def summarize(request: SummarizeRequest):

    logger.info("Summarization request received")

    try:
        # Split long text into chunks
        chunks = split_text_into_chunks(request.text)

        logger.info(
            "Text split into %d chunks",
            len(chunks),
        )

        # Generate summary
        summary = summarize_long_text(
            text=request.text,
            length=request.length,
            style=request.style,
        )

        logger.info("Summarization completed successfully")

        return {
            "summary": summary,
            "original_length": len(request.text),
            "summary_length": len(summary),
            "chunks_processed": len(chunks),
            "style": request.style,
            "length": request.length,
        }

    except genai_errors.APIError as exc:
        logger.exception("Gemini API error occurred")

        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=(
                f"Summarization service is unavailable " f"(upstream error {exc.code})."
            ),
        ) from exc

    except Exception:
        logger.exception("Unexpected error during summarization")

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred.",
        )
