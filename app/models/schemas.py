from pydantic import BaseModel, Field
from typing import Literal


class SummarizeRequest(BaseModel):
    text: str = Field(
        min_length=50,
        description="The text that needs to be summarized.",
        examples=[
            "Artificial intelligence is transforming many industries. "
            "It helps businesses automate tasks, analyze data, "
            "and improve decision-making."
        ],
    )

    length: Literal["short", "medium", "long"] = Field(
        default="medium",
        description="Desired summary length.",
        examples=["short"],
    )

    style: Literal[
        "professional",
        "casual",
        "academic",
        "bullet_points",
    ] = Field(
        default="professional",
        description="Writing style of the generated summary.",
        examples=["professional"],
    )


class SummarizeResponse(BaseModel):
    summary: str = Field(description="The generated summary.")

    original_length: int = Field(description="Character count of the original text.")

    summary_length: int = Field(description="Character count of the generated summary.")

    chunks_processed: int = Field(description="Number of text chunks processed.")

    style: str = Field(description="Writing style used.")

    length: str = Field(description="Requested summary length.")

    model_config = {
        "json_schema_extra": {
            "example": {
                "summary": "Artificial intelligence improves business efficiency through automation and data analysis.",
                "original_length": 150,
                "summary_length": 87,
                "chunks_processed": 1,
                "style": "professional",
                "length": "short",
            }
        }
    }
