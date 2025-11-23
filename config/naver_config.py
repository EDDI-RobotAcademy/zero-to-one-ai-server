import os
from dotenv import load_dotenv

load_dotenv()


NAVER_CLIENT_ID = os.getenv("NAVER_CLIENT_ID", "").strip()
NAVER_CLIENT_SECRET = os.getenv("NAVER_CLIENT_SECRET", "").strip()
NAVER_API_BASE = os.getenv("NAVER_API_BASE", "https://openapi.naver.com").rstrip("/")


def validate_naver_config() -> None:
    if not NAVER_CLIENT_ID:
        raise ValueError("NAVER_CLIENT_ID is not set")
    if not NAVER_CLIENT_SECRET:
        raise ValueError("NAVER_CLIENT_SECRET is not set")
