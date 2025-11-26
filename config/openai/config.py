import os
from dotenv import load_dotenv
from openai import OpenAI

# .env 파일 자동 로딩
load_dotenv()

# 환경변수에서 API 키 읽기
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY environment variable not set!")

# OpenAI 클라이언트 초기화
openai_client  = OpenAI(api_key=OPENAI_API_KEY)
