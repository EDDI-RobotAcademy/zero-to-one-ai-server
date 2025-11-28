import os
from dotenv import load_dotenv

from naver.bootstrap import setup_module as setup_naver
from product_review_crawling_agents.adapter.input.web.product_review_crawling_agents_router import \
    product_review_crawling_agents_router
from review.adapter.input.web.review_router import review_router

load_dotenv()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost:3000",  # Next.js 프론트 엔드 URL
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,       # 정확한 origin만 허용
    allow_credentials=True,      # 쿠키 허용
    allow_methods=["*"],         # 모든 HTTP 메서드 허용
    allow_headers=["*"],         # 모든 헤더 허용
)

app.include_router(product_review_crawling_agents_router, prefix="/product-reviews")
app.include_router(review_router, prefix="/review")

#모듈
setup_naver(app)

# 앱 실행
if __name__ == "__main__":
    import uvicorn
    host = os.getenv("APP_HOST")
    port = int(os.getenv("APP_PORT"))
    uvicorn.run(app, host=host, port=port)
