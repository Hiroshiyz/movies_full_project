from dotenv import load_dotenv
import os
# 載入.env檔案
load_dotenv()


class Config:
    # 從.env讀取
    TMDB_API_KEY = os.getenv('TMDB_API_KEY')
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev_key')
    SQLALCHEMY_DATABASE_URL = 'sqlite:///database.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
