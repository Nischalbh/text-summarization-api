from pydantic import BaseModel, Field
from typing import Literal


class SummarizeRequest(BaseModel):
    text: str = Field(min_length=50, description="Text that needs to be summarized")
    length: Literal["short", "medium", "long"] = "medium"
    style: Literal[
        "professional",
        "casual",
        "academic",
        "bullet_points",
    ] = "professional"


class SummarizeResponse(BaseModel):
    summary: str
    original_length: int
    summary_length: int
    chunks_processed: int
    style: str
    length: str
