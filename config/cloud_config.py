from dotenv import load_dotenv
import os

load_dotenv()

AWS_ACCESS_KEY_ID= os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY= os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_REGION= os.getenv("AWS_REGION")
AWS_S3_BUCKET= os.getenv("AWS_S3_BUCKET")
