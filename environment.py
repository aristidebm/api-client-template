import os
from dotenv import load_dotenv

load_dotenv(".env.example")  # or feth from settings.py if using django

BASE_URL = os.getenv("API_BASE_URL")
