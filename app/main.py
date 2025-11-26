import os
from dotenv import load_dotenv

# from anonymous_board.adapter.input.web.anonymous_board_router import anonymous_board_router
# from config.database.session import Base, engine
# from social_oauth.adapter.input.web.google_oauth2_router import authentication_router
# from account.adapter.input.web.account_router import account_router
from naver.adapter.input.web.naver_router import naver_router
from review.adapter.input.review_router import review_router

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

#app.include_router(anonymous_board_router, prefix="/board")
# app.include_router(authentication_router, prefix="/authentication")
# app.include_router(account_router, prefix="/account")
app.include_router(naver_router, prefix="/naver")
app.include_router(review_router, prefix="/review")
# 앱 실행
if __name__ == "__main__":
    import uvicorn
    host = os.getenv("APP_HOST")
    port = int(os.getenv("APP_PORT"))
    # Base.metadata.drop_all(bind=engine)
    # Base.metadata.create_all(bind=engine)
    uvicorn.run(app, host=host, port=port)
