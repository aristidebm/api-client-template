import os
import pathlib
from dotenv import load_dotenv

BASE_DIR = pathlib.Path(__file__).resolve().parent

# or feth from settings.py if using django
load_dotenv(BASE_DIR / ".env.example")

BASE_URL = os.getenv("API_BASE_URL")
