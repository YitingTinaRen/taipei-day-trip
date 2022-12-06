from flask import *
from flask_cors import CORS
from route.attraction_api import attraction_api
from route.account_api import account_api

app=None

app=Flask(__name__)
app.config["JSON_AS_ASCII"]=False
app.config["TEMPLATES_AUTO_RELOAD"]=True
app.config['JSONIFY_MIMETYPE'] ="application/json;charset=utf-8"
app.config["JSONIFY_PRETTYPRINT_REGULAR"]="True"
app.config["SECRET_KEY"]="TaipeiDayTripSecretKey"
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
app.register_blueprint(attraction_api, url_prefix="/")
app.register_blueprint(account_api, url_prefix="/")


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


app.run(host='0.0.0.0', port=3000, debug=False)

