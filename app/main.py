from fastapi import FastAPI, Depends, HTTPException, status
from google.genai import errors as genai_errors

from app.models.schemas import SummarizeRequest, SummarizeResponse
from app.services.summarizer import summarize_long_text
from app.text_chunker import split_text_into_chunks
from app.core.rate_limiter import rate_limit
from app.core.logger import logger

# API tags for Swagger documentation
tags_metadata = [
    {
        "name": "General",
        "description": "General application information and health checks.",
    },
    {
        "name": "Summarization",
        "description": "AI-powered text summarization operations.",
    },
]


# Create FastAPI application
app = FastAPI(
    title="Text Summarization API",
    description="""
    ## AI-Powered Text Summarization

    A REST API built with FastAPI and Google Gemini.

    ### Features
    - Summarize long text into short, medium, or long summaries.
    - Choose different writing styles.
    - API key authentication.
    - Redis-based rate limiting.
    - Long text processing and error handling.
    """,
    version="1.0.0",
    openapi_tags=tags_metadata,
)


# Home endpoint
@app.get(
    "/",
    summary="API Welcome",
    description="Returns a welcome message and application status.",
    tags=["General"],
)
def home():
    logger.info("Home endpoint accessed")

    return {
        "message": "Welcome to Text Summarization API",
        "status": "Running successfully",
    }


# Health check endpoint
@app.get(
    "/health",
    summary="Health Check",
    description="Checks whether the API application is running.",
    tags=["General"],
)
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
    summary="Summarize Text",
    description="""
    Generates an AI-powered summary of the provided text.

    **Requirements:**
    - Minimum text length: 50 characters.
    - Valid API key required.
    - Maximum 10 requests per minute per API key.

    **Supported lengths:** short, medium, long.

    **Supported styles:** professional, casual, academic, bullet_points.
    """,
    tags=["Summarization"],
    responses={
        401: {"description": "Missing or invalid API key."},
        422: {"description": "Input validation error."},
        429: {"description": "Rate limit exceeded."},
        502: {"description": "External Gemini API service error."},
        500: {"description": "Unexpected internal server error."},
    },
)
def summarize(request: SummarizeRequest):

    logger.info("Summarization request received")

    try:
        # Split long text into chunks
        chunks = split_text_into_chunks(request.text)

        logger.info("Text split into %d chunks", len(chunks))

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
