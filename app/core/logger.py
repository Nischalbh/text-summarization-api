import logging
import os

# create logs directory

os.makedirs("logs", exist_ok=True)

# configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("logs/app.log"), logging.StreamHandler()],
)
# Create application logger
logger = logging.getLogger("summarization_api")
