def split_text_into_chunks(text: str, max_chars: int = 5000):

    # Split text into individual words
    words = text.split()

    chunks = []
    current_chunk = []
    current_length = 0

    for word in words:

        # Calculate the length
        added_length = len(word) + (1 if current_chunk else 0)

        # Check whether adding this word exceeds the limit
        if current_chunk and current_length + added_length > max_chars:

            # Save the current chunk
            chunks.append(" ".join(current_chunk))

            # Start a new chunk
            current_chunk = []
            current_length = 0

        # Add the word to the current chunk
        current_chunk.append(word)
        current_length += len(word) + (1 if len(current_chunk) > 1 else 0)

    # Add the remaining words
    if current_chunk:
        chunks.append(" ".join(current_chunk))

    return chunks
