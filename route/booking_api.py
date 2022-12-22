from  flask import *
import model

booking_api = Blueprint('booking_api', __name__)


@booking_api.route("/api/booking", methods=["GET","POST", "DELETE"])
def booking():
    if request.method=="GET":
        token=request.cookies.get("user")
        result=model.USER.booking_not_confirmed(token)
        return result
    elif request.method=="POST":
        token = request.cookies.get("user")
        booking_data=request.get_json()
        result=model.USER.build_booking(booking_data, token)
        return result
    elif request.method =="DELETE":
        token = request.cookies.get("user")
        result=model.USER.delete_booking(token)
        return result

