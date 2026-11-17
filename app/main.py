from fastapi import FastAPI

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
