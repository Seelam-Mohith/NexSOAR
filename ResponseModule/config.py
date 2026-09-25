import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data" / "atomics"
DB_DIR = BASE_DIR / "db"
COLLECTION_NAME = "atomics"

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
