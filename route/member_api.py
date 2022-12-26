from flask import *
import model

member_api = Blueprint('member_api', __name__)


@member_api.route("api/member", methods=["POST", "DELETE"])
def member():
    if request.method=="POST":
        token = request.cookies.get("user")
        result=model.orders.check_order(token)
        return result
    else:
        token = request.cookies.get("user")
        booking_id=request.get_json("booking_id")
        result = model.orders.delete_order(token,booking_id)
        return result


