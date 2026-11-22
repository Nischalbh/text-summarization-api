import os
import secrets

from dotenv import load_dotenv
from fastapi import HTTPException, Security, status
from fastapi.security import APIKeyHeader

# Load environment variables
load_dotenv()

# Define API key authentication scheme
api_key_header = APIKeyHeader(
    name="X-API-Key",
    scheme_name="API Key Authentication",
    description="Enter your API key to access protected endpoints.",
    auto_error=False,
)


# Verify API key
async def verify_api_key(api_key: str | None = Security(api_key_header)):
    expected_api_key = os.getenv("CLIENT_API_KEY")

    if not expected_api_key:
        raise RuntimeError("CLIENT_API_KEY is missing from .env")

    if not api_key or not secrets.compare_digest(api_key, expected_api_key):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing API key",
        )

    return api_key
