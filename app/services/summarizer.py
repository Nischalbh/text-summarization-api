from app.services.gemini_service import combine_summaries, generate_summary
from app.text_chunker import split_text_into_chunks


def summarize_chunks(chunks: list[str], length: str, style: str) -> list[str]:
    """Summarize each text chunk with Gemini."""
    return [
        generate_summary(text=chunk, length=length, style=style)
        for chunk in chunks
    ]


def summarize_long_text(text: str, length: str, style: str) -> str:
    """Split text, summarize every chunk, then merge into one final summary."""
    chunks = split_text_into_chunks(text)
    chunk_summaries = summarize_chunks(chunks, length, style)

    if len(chunk_summaries) == 1:
        return chunk_summaries[0]

    return combine_summaries(
        summaries=chunk_summaries,
        length=length,
        style=style,
    )
