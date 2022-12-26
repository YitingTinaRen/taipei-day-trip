import os
from dotenv import load_dotenv

load_dotenv()

# Database configuration
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_DB = os.getenv('DB_DB')
DB_POOL_NAME=os.getenv('DB_POOL_NAME')
DB_POOL_SIZE=20

# Flask app configuration
DEBUG = os.getenv('DEBUG')
PORT = os.getenv('PORT')
HOST = os.getenv('HOST')
SECRET_KEY = os.getenv('SECRET_KEY')
JSON_AS_ASCII=False
TEMPLATES_AUTO_RELOAD=True
JASONIFY_MIMETYPE='application/json;charset=utf-8'
JSON_PRETTYPRINT_REGULAR="True"

# jwt algorithm
JWT_ALGO=os.getenv('JWT_ALGO')










# # Database configuration
# DB_USER = 'root'
# DB_PASSWORD = '0000'
# DB_HOST = 'localhost'
# DB_DB = 'TaipeiDayTrip'
# DB_POOL_NAME='mypool'
# DB_POOL_SIZE=20

# # Flask app configuration
# DEBUG = True
# PORT = 3000
# HOST = "0.0.0.0"
# SECRET_KEY = "TaipeiDayTripSecretKey"
# JSON_AS_ASCII=False
# TEMPLATES_AUTO_RELOAD=True
# JASONIFY_MIMETYPE='application/json;charset=utf-8'
# JSON_PRETTYPRINT_REGULAR="True"

# # jwt algorithm
# JWT_ALGO='HS256'
