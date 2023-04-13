from flask import *
import model

order_api = Blueprint('order_api', __name__)


@order_api.route("api/orders", methods=["POST"])
def orders():
    token = request.cookies.get("user")
    orders = request.get_json()
    result = model.orders.make_order(token, orders)
    print(result)
    return result


@order_api.route("api/order/<orderNumber>", methods=["GET"])
def getOrderNumber(orderNumber):
    token = request.cookies.get("user")
    if not token:
        return jsonify({"error": True, "message": "User not logs in."}), 403
    auth = model.USER.auth(token)
    auth = json.loads(auth[0].data)
    print(auth)
    if "error" in auth:
        return jsonify({"error": True, "message": auth["message"]}), 403

    result = model.db.get_order_by_orderNum(orderNumber)
    print(result)
    if result:
        return jsonify({"data": {"number": result[0]["order_num"],
                                 "price": result[0]["price"], "trip": {
            "attraction": {
                        "id": result[0]["id"],
                        "name": result[0]["name"],
                        "address": result[0]["address"],
                        "image": result[0]["images"]
                        },
            "date": f'{result[0]["date"]:%Y-%m-%d}',
                    "time": result[0]["time"]
        },
            "contact": {
            "name": result[0]["username"],
            "email": result[0]["email"],
            "phone": result[0]["phone"]
        },
            "status": result[0]["transaction_status"]
        }}), 200
    else:
        return jsonify(None), 200
