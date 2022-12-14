from flask import jsonify, make_response
import re
import jwt
from datetime import datetime, timedelta
import model
import config
import json

class USER:
    def register(username, email, psw):

        if not username or not email or not psw:
            return jsonify({"error":True, "message": "Please fill out the form."}), 400
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            return jsonify({"error":True, "message": "Invalid email."}), 400
        elif model.db.search_member_by_email(email):
            return jsonify({"error": True, "message":"Email already exists."}), 400
        else:
            if model.db.register(username, email, psw):
                return jsonify({"ok":True}),200
            else:
                return jsonify({"error":True, "message":"Server internal error."}), 500
    
    def login(email, password):
        DB_result=model.db.search_member_by_email(email)
        if not email or not password:
            return jsonify({"error":True, "message":"Please fill out the form."}), 400

        if not DB_result:
            return jsonify({"error":True, "message":"Email does not exist."}), 400
        elif password == DB_result["password"]:
            # Create JWT token
            token=jwt.encode({
                'userID':DB_result["member_id"],
                'username':DB_result["username"],
                'email':email,
                'exp':datetime.utcnow()+timedelta(minutes=30)
            },
            config.SECRET_KEY, algorithm=config.JWT_ALGO)
            
            # Save to cookie
            res=make_response(jsonify({"ok": True}),200)
            res.set_cookie('user', token)
            return res
        else:
            return jsonify({"error":True, "message":"Wrong password."}), 400

    def auth(token):
        if not token:
            return jsonify(None), 200
        
        try:
            data=jwt.decode(token, config.SECRET_KEY, algorithms=config.JWT_ALGO)
        except jwt.exceptions.InvalidTokenError as error:
            print(error)
            return jsonify({"error":True, "message":"Invalid token"}), 400
        return jsonify({"data":{"id":data["userID"], "name":data["username"],"email":data["email"]}}), 200

    def delete_token():
        res=make_response(jsonify({"ok": True}),200)
        res.delete_cookie('user')
        return res
    
    def booking_not_confirmed(token):
        if not token:
            return jsonify({"error": True, "message": "User not log in."}), 403
        
        user_data = USER.auth(token)
        user_data=json.loads(user_data[0].data)
        if "error" in user_data:
            return jsonify({"error": True, "message": user_data["message"]}), 400
        
        result = model.db.check_booking(user_data['data']['id'])
        if not result:
            return jsonify(None), 200
        else:
            return jsonify({"data": {"attraction": {"id": result[0]["id"], "name": result[0]["name"], "address": result[0]["address"], "image": result[0]["images"]}, "date": f'{result[0]["date"]:%Y-%m-%d}', "time": result[0]["time"], "price": result[0]["price"]}}), 200

    def build_booking(booking_data, token):
        if not token:
            return jsonify({"error": True, "message": "User not log in."}), 403

        if not booking_data["date"] or not booking_data["time"] or not booking_data["price"]:
            return jsonify({"error":True, "message":"Please fill out the form."}), 400

        user_data = USER.auth(token)
        user_data = json.loads(user_data[0].data)
        if "error" in user_data:
            return jsonify({"error":True, "message":user_data["message"]}), 400

        has_book_history=model.db.check_booking(user_data["data"]["id"])
        if not has_book_history:
            result=model.db.build_booking(user_data["data"]["id"], booking_data["attractionId"], 
                                        booking_data["date"],booking_data["time"], booking_data["price"])
        else:
            result = model.db.update_booking(user_data["data"]["id"], booking_data["attractionId"],
                                          booking_data["date"], booking_data["time"], booking_data["price"])
        
        if result:
            return jsonify({"ok":True}), 200
        else:
            return jsonify({"error":True, "message":"Server internal error"}), 500


    def delete_booking(token):
        if not token:
            return jsonify({"error": True, "message": "User not log in."}), 403
        
        user_data = USER.auth(token)
        user_data = json.loads(user_data[0].data)
        # print(user_data)
        if "error" in user_data:
            return jsonify({"error": True, "message": user_data["message"]}), 400

        result = model.db.delete_booking(user_data["data"]["id"])
        if result:
            return jsonify({"ok": True}), 200
        else:
            return jsonify({"error": True, "message": "Server internal error"}), 500
