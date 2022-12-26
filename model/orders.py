from flask import jsonify, make_response
import jwt
from datetime import datetime, timedelta
import model
import config
import json
import requests
import re

class orders:
    def make_order(token, data):
        token_info=model.USER.auth(token)
        token_info=json.loads(token_info[0].data)

        if "error" in token_info:
            return jsonify({"error": True, "message": token_info["message"]}), 403

        if not token_info["data"]["name"] == data["contact"]["name"] or not token_info["data"]["email"] == data["contact"]["email"]:
            return jsonify({"error": True, "message": "User name and email conflict with contact information."}), 400
        elif not re.match(r'09\d{8}', data["contact"]["phone"]):
            return jsonify({"error": True, "message": "Wrong phone format."}), 400
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', data["contact"]["email"]):
            return jsonify({"error": True, "message": "Invalid email."}), 400

        # create order number and bank transaction id
        orderNum = orders.create_order_num()
        bank_trans_id= orders.create_bank_transaction_id()

        res=orders.pay_by_prime(data, bank_trans_id, orderNum)

        booking_info = model.db.check_booking(token_info["data"]["id"])
        booking_id = booking_info[0]["booking_id"]

        if model.db.record_order(res, booking_id, data["contact"]["phone"]) and not res["status"] and model.db.confirm_booking(token_info["data"]["id"]):
            return jsonify({"data": {"number": res["order_number"], "payment": {
                          "status": res["status"], "message": "付款成功"}}}), 200
        else:
            return jsonify({"error":True, "message":"伺服器內部錯誤"}), 500

    def create_order_num():  
        # create order number from time
        now = datetime.now()
        orderNum = datetime.strftime(now, '%Y%m%d%H%M%S%f')
        return orderNum

    def create_bank_transaction_id():
        now = datetime.now()
        bank_trans_id = datetime.strftime(now, '%Y%m%d%H%M%S')
        return "B"+bank_trans_id
    
    def pay_by_prime(data,bank_transaction_id, order_num):
        url = 'https://sandbox.tappaysdk.com/tpc/payment/pay-by-prime'
        Headers = {"Content-Type": 'application/json',
                   'x-api-key': 'partner_qYMTbDi8hZm1fB3UkHDG3FOQHZ5QWZGfRMwndUE7HdMBJ5yLuYk6kBFV'
                   }
        payload = {
            "partner_key": "partner_qYMTbDi8hZm1fB3UkHDG3FOQHZ5QWZGfRMwndUE7HdMBJ5yLuYk6kBFV",
            "prime": data["prime"],
            # "prime": "test_3a2fb2b7e892b914a03c95dd4dd5dc7970c908df67a49527c0a648b2bc9",
            "amount": data["order"]["price"],
            "merchant_id": "yiting2022_CTBC",
            "details": "TaipeiDayTrip",
            "bank_transaction_id": bank_transaction_id,
            "cardholder": {
                "phone_number": data["contact"]["phone"],
                "name": data["contact"]["name"],
                "email": data["contact"]["email"],

            },
            "order_number": order_num
        }

        res = requests.post(url, headers=Headers, data=json.dumps(payload))
        res = res.json()
        return res

    def check_order(token):
        token_info = model.USER.auth(token)
        token_info = json.loads(token_info[0].data)
        if "error" in token_info:
            return jsonify({"error": True, "message": token_info["message"]}), 403
        
        result=model.db.get_member_order(token_info["data"]["id"])
        return jsonify(result), 200

    def delete_order(token, booking_id):
        token_info = model.USER.auth(token)
        token_info = json.loads(token_info[0].data)
        if "error" in token_info:
            return jsonify({"error": True, "message": token_info["message"]}), 403
        
        rec_trade_id=model.db.get_refund_id(booking_id)
        refundResult=orders.tapPayRefund(rec_trade_id)
        print(refundResult)

        result = model.db.delete_order(booking_id,token_info["data"]["id"])
        if result and refundResult["status"] ==0:
            return jsonify({"ok":True}), 200
        elif refundResult['status'] !=0:
            return jsonify({"error":True, "message":refundResult["msg"]}), 500
        elif not result:
            return jsonify({"error":True, "message":"Database issue"}), 500

    def tapPayRefund(rec_trade_id):
        url = 'https://sandbox.tappaysdk.com/tpc/transaction/refund'
        Headers = {"Content-Type": 'application/json',
                   'x-api-key': 'partner_qYMTbDi8hZm1fB3UkHDG3FOQHZ5QWZGfRMwndUE7HdMBJ5yLuYk6kBFV'
                   }
        payload = {
            "partner_key": "partner_qYMTbDi8hZm1fB3UkHDG3FOQHZ5QWZGfRMwndUE7HdMBJ5yLuYk6kBFV",
            "rec_trade_id":rec_trade_id
        }

        res = requests.post(url, headers=Headers, data=json.dumps(payload))
        res = res.json()
        return res
