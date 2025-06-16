import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GPT_MODEL = "gpt-4"  # or "gpt-3.5-turbo"
IMAGE_SIZE = "1024x1024"
