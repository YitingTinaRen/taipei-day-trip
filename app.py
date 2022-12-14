from flask import *
from flask_cors import CORS
from route.attraction_api import attraction_api
from route.account_api import account_api
from route.booking_api import booking_api
import config

app=None

app=Flask(__name__)
app.config.from_object(config)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
app.register_blueprint(attraction_api, url_prefix="/")
app.register_blueprint(account_api, url_prefix="/")
app.register_blueprint(booking_api, url_prefix="/")


# Pages
@app.route("/")
def index():
	return render_template("index.html")
@app.route("/attraction/<id>")
def attraction(id):
	return render_template("attraction.html")
@app.route("/booking")
def booking():
	return render_template("booking.html")
@app.route("/thankyou")
def thankyou():
	return render_template("thankyou.html")


app.run(host=config.HOST, port=config.PORT, debug=config.DEBUG)

