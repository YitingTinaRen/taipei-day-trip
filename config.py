# Database configuration
DB_USER = 'root'
DB_PASSWORD = '0000'
DB_HOST = 'localhost'
DB_DB = 'TaipeiDayTrip'
DB_POOL_NAME='mypool'
DB_POOL_SIZE=20

# Flask app configuration
DEBUG = False
PORT = 3000
HOST = "0.0.0.0"
SECRET_KEY = "TaipeiDayTripSecretKey"
JASON_AS_ASCII=False
TEMPLATES_AUTO_RELOAD=True
JASONIFY_MIMETYPE='application/json;charset=utf-8'
JSON_PRETTYPRINT_REGULAR="True"

# jwt algorithm
JWT_ALGO='HS256'
