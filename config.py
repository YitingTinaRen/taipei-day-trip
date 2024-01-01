import os
from dotenv import load_dotenv

load_dotenv()

# Database configuration
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_DB = os.getenv("DB_DB")
DB_POOL_NAME = os.getenv("DB_POOL_NAME")
DB_POOL_SIZE = 10
SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI")

# Flask app configuration
DEBUG = os.getenv("DEBUG")
PORT = os.getenv("PORT")
HOST = os.getenv("HOST")
SECRET_KEY = os.getenv("SECRET_KEY")
JSON_AS_ASCII = False
TEMPLATES_AUTO_RELOAD = True
JASONIFY_MIMETYPE = "application/json;charset=utf-8"
JSON_PRETTYPRINT_REGULAR = "True"

# jwt algorithm
JWT_ALGO = os.getenv("JWT_ALGO")

# LIFF_ID
LIFF_ID = os.getenv("LIFF_ID")
LIFF_CHANEL_SECRET = os.getenv("LIFF_CHANEL_SECRET")
LINE_CHANNEL_ACCESS_TOKEN = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")
LINE_CHANEL_ID = os.getenv("LINE_CHANEL_ID")
