from flask import *
from flask_cors import CORS
import route
import config
from liff.views import liff_blueprint

app = None

app = Flask(__name__)
app.config.from_object(config)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
app.register_blueprint(route.attraction_api, url_prefix="/")
app.register_blueprint(route.account_api, url_prefix="/")
app.register_blueprint(route.booking_api, url_prefix="/")
app.register_blueprint(route.order_api, url_prefix="/")
app.register_blueprint(route.member_api, url_prefix="/")
app.register_blueprint(liff_blueprint, url_prefix="/liff/")


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


@app.route("/member")
def member():
    return render_template("member.html")


app.run(host=config.HOST, port=config.PORT, debug=config.DEBUG)
