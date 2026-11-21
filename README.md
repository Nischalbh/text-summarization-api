# Text Summarization API

An AI-powered text summarization API built using **FastAPI** and **Google Gemini**. It allows users to summarize long text into shorter, meaningful summaries with different lengths and writing styles.

## Features

- AI-powered text summarization using Google Gemini
- Short, medium, and long summary options
- Multiple writing styles: Professional, Casual, Academic, and Bullet Points
- Long text processing using text chunking
- API key authentication
- Redis-based rate limiting
- Application logging
- Input validation using Pydantic
- Error handling for upstream API failures
- Automated testing using Pytest

## Tech Stack

- **Backend:** Python, FastAPI
- **AI Model:** Google Gemini
- **Database/Cache:** Redis
- **Validation:** Pydantic
- **Testing:** Pytest, HTTPX
- **API Documentation:** Swagger UI

## Project Structure

```text
app/
├── core/
│   ├── security.py
│   ├── redis_client.py
│   ├── rate_limiter.py
│   └── logger.py
├── models/
│   └── schemas.py
├── services/
│   └── summarizer.py
├── main.py
└── text_chunker.py

tests/
└── test_main.py

logs/
requirements.txt
.env
```

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/Nischalbh/text-summarization-api.git
cd text-summarization-api
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

### 3. Activate the virtual environment

Windows:

```bash
venv\Scripts\activate
```

### 4. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 5. Configure environment variables

Create a `.env` file in the project root and configure the required variables:

```env
GEMINI_API_KEY=your_gemini_api_key
CLIENT_API_KEY=your_client_api_key
REDIS_URL=redis://localhost:6379
```

Never commit your `.env` file or expose API keys publicly.

### 6. Start Redis

Make sure Docker Desktop is running, then execute:

```bash
docker run -d --name redis-server -p 6379:6379 redis:7-alpine
```

### 7. Run the application

```bash
python -m uvicorn app.main:app --reload
```

The API will be available at:

`http://127.0.0.1:8000`

## API Documentation

Swagger UI:

`http://127.0.0.1:8000/docs`

## Main Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Welcome message |
| GET | `/health` | Health check |
| POST | `/api/v1/summarize` | Summarize text |

## Authentication

The summarization endpoint requires an API key.

Add this header to your request:

```http
X-API-Key: your_client_api_key
```

## Example Request

```json
{
  "text": "Your text with at least 50 characters goes here...",
  "length": "short",
  "style": "professional"
}
```

## Run Tests

```bash
python -m pytest -v
```

## Error Handling

| Status Code | Description |
|---|---|
| 200 | Successful request |
| 401 | Missing or invalid API key |
| 422 | Input validation error |
| 429 | Rate limit exceeded |
| 502 | Upstream AI service error |
| 500 | Unexpected server error |

## Author

**Nischal Bhattarai**

GitHub: https://github.com/Nischalbh