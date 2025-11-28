from fastapi import APIRouter
import json

from product_review_crawling_agents.application.usecase.product_review_crawling_agents_usecase import \
    ProductReviewAgentsUseCase
from review.adapter.input.web.request.SummaryRequest import SummaryRequest
from review.adapter.input.web.response.SummaryResponse import SummaryResponse, ProductSummary
from review.adapter.output.llm_adapter import LLMAdapter
from review.adapter.output.pdf_adapter import PdfAdapter
from review.adapter.output.s3_upload_adapter import S3UploaderAdapter
from review.application.usecase.pdf_usecase import PdfUseCase
from review.application.usecase.summarize_usecase import SummarizeUseCase
from review.domain.pdf_document import PdfDocument
from review.infrastructure.client.openai_client import OpenAIClient
from config.openai.config import openai_client

review_router = APIRouter()
client = OpenAIClient(openai_client)
summarizeUsecase = SummarizeUseCase(LLMAdapter(client))
naverReviewCrawlingUsecase = ProductReviewAgentsUseCase()
# preprocessUsecase = ();
pdfUsecase = PdfUseCase(PdfAdapter(), S3UploaderAdapter())


@review_router.post("/summary", response_model=SummaryResponse)
async def analyze_product(data: SummaryRequest):
    # 1. 크롤링
    raw_reviews = await naverReviewCrawlingUsecase.crawling_naver_review_agents(data.info_url)
    # print("크롤링 된 데이터-------------------------")
    # print(raw_reviews)

    # 2. 전처리
    # clean_reviews = preprocessUsecase.execute(raw_reviews)

    # 3. 요약
    # summary_result = summarizeUsecase.summarize_review(clean_reviews)

    preprocessed_reviews = [
        "아이 생일선물로 여러가지 문구류구매했는데 필기구는 많이 안들어가겠지만 귀여워요",
        "아이가 너무좋아해요 단점은 안에 새연필들어갈때 길이가 꽉 끼는거같아요",
        "아이들이 엄청 좋아 하네요~좋은상품 감사~",
        "아이들이 엄청 좋아하네요~좋은상품 감사~",
        "잘 받았습니다. 저렴하게 잘 샀습니다.",
        "잘 받았습니다. 저렴하게 잘 샀습니다. 기대이상이네요~아이들이 넘 좋아하네요~~^^",
        "딸램이 너무 좋아해요 ㅋㅋ 근데 연필거의 안들어가서 인형으로씀",
        "딸아이가 필통으로 잘 사용하고 있어요",
        "친구들끼리 색깔별로 가지고 논다고 사달라고해서 사주었어요. 애착템이 되었어요.",
        "귀엽습니다. 색상도 만족합니다.",
        "두딸 친구들 선물로 넘 좋아요~~",
        "두딸 친구들 선물로 넘 좋아요~~",
        "두딸 친구들 선물로 넘 좋아요~~",
        "너무 귀여워용! 털도 너무 부드러워용💚",
        "너무 귀여워용! 털도 너무 부드러워용💚",
        "너무 귀여워용! 털도 너무 부드러워용💚",
        "너무 귀여워용! 털도 너무 부드러워용💚",
        "잘 받았어요. 토끼인형이 생각보다 좀 큰데 아이는 좋아합니다ㅎㅎ",
        "조카 선물 했는데 너무 좋아하더라고요. 실제로 보니 필통보다는 안쪽도 폭신하니 인형 같아서 더 좋아하더라고요.",
        "토끼인형을 좋아하는 딸이 너무 좋아해요~~~~",
        "배송도 빠 르고 제품 좋습니다",
        "토끼 필통 귀여워요~~~~~",
        "생각보다 귀여워여 ㅎㅎ",
        "실제가 사진과 같구요. 너무너무 귀여워요~~~👍👍👍배송도 빨랐습니다.",
        "좋아요 정말 감사드립니다",
        "좋아요~~~~~~~~",
        "즈히집애기가 젤좋아하는 인형이에요 ㅋㅋ",
        "초등학교4학년 딸아이가 사고싶어해서 사주었더니 너무 좋아합니다 촉감도 보들보들 하고 필통으로 시용하기 아까울 정도로 퀄리티 좋습 니당",
        "제가 산거 보고 친구들이 귀엽다고 난리라 친구들이랑 나눠 가지려고 10개 주문했어요~! 보들보들 촉감 너무 좋고, 색상도 실물 너무 예뻐요😍 안에 필기구 제법 들어가요~",
        "딸아이가 너무  좋아해요",
        "항상 구매중입니다 너무 좋아용",
        "아이들이 너무좋아해요 앙증맞은 꼬리지퍼 센스",
        "초딩 친구들 생일선물로 주기 너무 좋아요 받으면 모두 대만족이라 재구매합니다",
        "꼬리로 지퍼를 여닫을 수 있어서 귀여워요",
        "필통인데 인형처럼 예뻐요. 색상 고루 예뻐요",
        "필통인데 인형처럼 예뻐요. 색상 고루 예뻐요",
        "필통인데 인형처럼 예뻐요. 색상 고루 예뻐요",
        "필통 인데 인형처럼 예뻐요. 색상 고루 예뻐요",
        "아이가. 좋아하네요",
        "딸이랑 조카 사줬어요 털이 엄청 부드럽습니다 진짜 인형같아요^^",
        "큼직한게 인형처럼 예뻐요",
        "아이가 좋아해요|~~",
        "아이들이 만족해 합니다 배송도 빠르고",
        "아이들이 만족해 합니다 배송도 빠르고",
        "정말 이쁘네요 우와",
        "정말 이쁘네요 우와",
        "정말 이쁘네요 우와",
        "정말 이쁘네요 우와",
        "정말 이쁘네요 우와",
        "촉감도좋고 아이가 좋아하네요^^ 인형같아서 더 좋아하는것같아요",
        "아이들이 좋아했어요! 다양한 아이템을 합리적인 가격에 살 수 있어서 아이들 선물할 일 있을때 늘 애용해요!",
        "넘 부들부들하고 귀여워요ㅎ",
        "딸아이가 사고싶어해서 인형처럼 잘들고다니네요",
        "예쁘게 잘쓰고 있습니다. 제 생각보다는 사이즈가 커요.",
        "진짜 귀여워요!!!! 다들 인형테라피하세요",
        "아주 만족해요 아이가 좋아하네요",
        "왕크왕귀에요~!!! 털도 부드럽고 귀엽네요 ₩",
        "귀여워요~!!! 생각없이 계속 만지게되네요~!!",
        "아이가 너무너무 좋아합니다.",
        "구디백으로 주문했어요. 친구들이 좋아했으면 좋겠네요",
        "애들이 좋아해서 몇개 샀어요",
        "크기는 생각보다 커요 아이가좋아하고요~~ 특성상안에 편을 넣고 빼고는 쉽지않아요! 이쁜걸로 만족합니다",
        "딸래 미가 엄청 좋아하지요~",
        "조카들 선물로 주었는데, 너무너무 좋아했어요,,,♡",
        "조카들 선물로 주었는데, 너무너무 좋아했어요,,,♡",
        "배송도 빠르고 너무 이뻐요~~",
        "조카 생일선물로 주문했어요 배송도 빠르고 선물 마음에 들어해서 기쁘네요.",
        "학원 어린이날 행사때 작년에 여기 사이트에서 구매 했는데 올해도 구매하네요 !",
        "학원 어린이날 행사때 작년에 여기 사이트에서 구매 했는데 올해도 구매하네요 !",
        "좋아요아이가 좋아행ㅅ",
        "토끼인형필통 선물 좋습니더",
        "배송도 빠르고 상품도 좋아요",
        "귀여운데 엄청 커요 그리고 사이즈에 비해 필통공간이 너무좁아여ㅠㅠ  토끼배 터질려고해여…",
        "너무 귀여워요 아이가 좋아할 거 같아요",
        "딸이 좋아해요 다음에도 기회가 되면 다시 구매하도록 하겠습니다 감사합니다 많이 파세요 수고하세요",
        "귀엽고 필통으로도 사용할 수 있어서 좋아요",
        "너무너무좋아요너무너무",
        "매우만족합니다 잘사용중",
        "선물했는데귀여워영~~~",
        "아이가 너무 좋아합니다. 가격대비 상품도 좋아요. 인형으로도 쓰고 있어요 인형인지 필통인지 헷갈려요 ㅎㅎ",
        "아이가좋아해요저렴하게잘샀어요",
        "아이가좋아해요저렴하게잘샀어요",
        "귀여워요 조카선물로 삿어요",
        "귀여운데 생각보다 커요 딸아이 주려고 구매했어요 색은 다른색이랑 섞어살걸 조금 후회되네요",
        "너무너무좋아요좋아요",
        "예쁘고 귀여워요ㅠ 근데 가방에 달고 다니고 싶었는데 생각보다 너어무 크네요ㅋㅋ",
        "사이즈가 약간 커요. 인형인듯 필통인듯~아이는 무지 좋아해요",
        "배송빠르고 이쁘네용 아이가 좋아해요",
        "아이가 너무너무 좋아하는 토끼필통",
        "넘 귀여워요... 보들보들하고 색도 귀엽고!! 다만 생각한 것보다 많이 커요..ㅋㅋ",
        "딸이 필통이 필요하대서 골랐는데 필통 겸 인형이라 가방에 달고 다녀요 친구들이 예쁘다고 한대요^^",
        "폭신폭신하고 예쁘게 생겼어요! 다만 필기구가 그리 많이 들어가지는 않습니다..!",
        "엄청 부드럽고 귀여워요 초등학교 저학년 선물했는데 좋아했어요 토끼가 꽤 커요 연필은 안들어 가지만 생긴게 귀여워서 마음에 들어요",
        "아이가 좋아하네요. 감사합니다.",
        "아이가 좋아하네요 만족",
        "아이가 너무 좋아해요 대 만족입니다. 번창하세요",
        "아이가 너무 좋아해요 귀엽고 보들보들해서 좋습니다. 번창하세요.",
        "아이가 좋아합니다 만족",
        "아이가 좋아해요~~",
        "털 부들부들해서 만질때마다 느낌이 너무 좋아요. 크기도 크고, 아이도 좋아합니다. 핑크색상 예뻐요"
    ]
    preprocessed_text = " ".join(preprocessed_reviews) # 이것도 전처리에서 하기
    
    summary_result = summarizeUsecase.summarize_review(data.name, preprocessed_text)  # LLM 반환값 

    # 4. PDF 생성 + S3 업로드
    # pdf_result = pdfUsecase.execute(data.name, data.price, summary_result)

    # TODO: 이걸 유스케이스 안에서 해야할지 의논
    pdf_document = PdfDocument(
        name=data.name,
        price=data.price,
        # thumbnail_url=data.thumbnail_url
        summary=summary_result["summary"],
        positive_features=summary_result["positive_features"],
        negative_features=summary_result["negative_features"],
        keywords=summary_result["keywords"]
    )

    pdf_result = pdfUsecase.execute(pdf_document)

    return SummaryResponse(
        product_summary=ProductSummary(
            name=data.name,
            price=data.price,
            summary=summary_result["summary"],
            positive_features=summary_result["positive_features"],
            negative_features=summary_result["negative_features"],
            keywords=summary_result["keywords"]
        ),
        pdf_url=pdf_result["url"]
    )



