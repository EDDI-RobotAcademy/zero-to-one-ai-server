# from domain.review import RawReview
#
# class ReviewSummary:
#     @staticmethod
#     def from_json(json_data: dict) -> list[RawReview]:
#         """JSON → RawReview 변환"""
#         reviews = []
#         for key, value in json_data.items():
#             reviews.append(RawReview(id=str(key), text=value))
#         return reviews