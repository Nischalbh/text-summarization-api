import os
from dotenv import load_dotenv
from redis.asyncio import Redis

# load environment
load_dotenv()
# Redis server URL
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
# REDIS Connection
redis_client = Redis.from_url(REDIS_URL, decode_responses=True)
