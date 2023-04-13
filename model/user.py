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
            return jsonify(
                {"error": True, "message": "Please fill out the form."}), 400
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            return jsonify({"error": True, "message": "Invalid email."}), 400
        elif model.db.search_member_by_email(email):
            return jsonify(
                {"error": True, "message": "Email already exists."}), 400
        else:
            if model.db.register(username, email, psw):
                return jsonify({"ok": True}), 200
            else:
                return jsonify(
                    {"error": True, "message": "Server internal error."}), 500

    def login(email, password):
        DB_result = model.db.search_member_by_email(email)
        if not email or not password:
            return jsonify(
                {"error": True, "message": "Please fill out the form."}), 400

        if not DB_result:
            return jsonify(
                {"error": True, "message": "Email does not exist."}), 400
        elif password == DB_result["password"]:
            # Create JWT token
            token = jwt.encode({
                'userID': DB_result["member_id"],
                'username': DB_result["username"],
                'email': email
            },
                config.SECRET_KEY, algorithm=config.JWT_ALGO)

            # Save to cookie
            res = make_response(jsonify({"ok": True}), 200)
            res.set_cookie('user', token)
            return res
        else:
            return jsonify({"error": True, "message": "Wrong password."}), 400

    def auth(token):
        if not token:
            return jsonify(None), 200

        try:
            data = jwt.decode(
                token,
                config.SECRET_KEY,
                algorithms=config.JWT_ALGO)
        except jwt.exceptions.InvalidTokenError as error:
            print(error)
            return jsonify({"error": True, "message": "Invalid token"}), 400
        return jsonify({"data": {
                       "id": data["userID"], "name": data["username"], "email": data["email"]}}), 200

    def delete_token():
        res = make_response(jsonify({"ok": True}), 200)
        res.delete_cookie('user')
        return res

    def booking_not_confirmed(token):
        if not token:
            return jsonify({"error": True, "message": "User not log in."}), 403

        user_data = USER.auth(token)
        user_data = json.loads(user_data[0].data)
        if "error" in user_data:
            return jsonify(
                {"error": True, "message": user_data["message"]}), 400

        result = model.db.check_booking(user_data['data']['id'])
        if not result:
            return jsonify(None), 200
        else:
            return jsonify({"data": {"attraction": {"id": result[0]["id"], "name": result[0]["name"], "address": result[0]["address"],
                           "image": result[0]["images"]}, "date": f'{result[0]["date"]:%Y-%m-%d}', "time": result[0]["time"], "price": result[0]["price"]}}), 200

    def build_booking(booking_data, token):
        if not token:
            return jsonify({"error": True, "message": "User not log in."}), 403

        if not booking_data["date"] or not booking_data["time"] or not booking_data["price"]:
            return jsonify(
                {"error": True, "message": "Please fill out the form."}), 400

        user_data = USER.auth(token)
        user_data = json.loads(user_data[0].data)
        if "error" in user_data:
            return jsonify(
                {"error": True, "message": user_data["message"]}), 400

        has_book_history = model.db.check_booking(user_data["data"]["id"])
        if not has_book_history:
            result = model.db.build_booking(
                user_data["data"]["id"],
                booking_data["attractionId"],
                booking_data["date"],
                booking_data["time"],
                booking_data["price"])
        else:
            result = model.db.update_booking(
                user_data["data"]["id"],
                booking_data["attractionId"],
                booking_data["date"],
                booking_data["time"],
                booking_data["price"])

        if result:
            return jsonify({"ok": True}), 200
        else:
            return jsonify(
                {"error": True, "message": "Server internal error"}), 500

    def delete_booking(token):
        if not token:
            return jsonify({"error": True, "message": "User not log in."}), 403

        user_data = USER.auth(token)
        user_data = json.loads(user_data[0].data)
        # print(user_data)
        if "error" in user_data:
            return jsonify(
                {"error": True, "message": user_data["message"]}), 400

        result = model.db.delete_booking(user_data["data"]["id"])
        if result:
            return jsonify({"ok": True}), 200
        else:
            return jsonify(
                {"error": True, "message": "Server internal error"}), 500

    def update_user_info(data, token):
        if not token:
            return jsonify({"error": True, "message": "User not log in."}), 403

        user_data = USER.auth(token)
        user_data = json.loads(user_data[0].data)
        if data["username"]:
            if data["username"] == user_data["data"]["name"]:
                return jsonify(
                    {"error": True, "message": "New name is the same as the old name."}), 400

            result = model.db.update_member(
                user_data["data"]["id"],
                data["username"],
                data["email"],
                data["newPsw"])
            # Create JWT token
            token = jwt.encode({
                'userID': user_data["data"]["id"],
                'username': data["username"],
                'email': user_data["data"]["email"]
            },
                config.SECRET_KEY, algorithm=config.JWT_ALGO)

            # Save to cookie
            res = make_response(
                jsonify({"ok": True, "message": "更新成功"}), 200)
            res.set_cookie('user', token)
            return res

        if data["email"]:
            if not re.match(r'[^@]+@[^@]+\.[^@]+', data["email"]):
                return jsonify(
                    {"error": True, "message": "Invalid email."}), 400
            elif model.db.search_member_by_email(data["email"]):
                return jsonify(
                    {"error": True, "message": "Email already exists."}), 400
            else:
                result = model.db.update_member(
                    user_data["data"]["id"],
                    data["username"],
                    data["email"],
                    data["newPsw"])
                # Create JWT token
                token = jwt.encode({
                    'userID': user_data["data"]["id"],
                    'username': user_data["data"]["name"],
                    'email': data["email"]
                },
                    config.SECRET_KEY, algorithm=config.JWT_ALGO)

                # Save to cookie
                res = make_response(
                    jsonify({"ok": True, "message": "更新成功"}), 200)
                res.set_cookie('user', token)
                return res

        if data["oldPsw"] and data["newPsw"]:
            if data["oldPsw"] == data["newPsw"]:
                return jsonify(
                    {"error": True, "message": "New password is the same as the old one."}), 400

            memberInfoDB = model.db.search_member_by_email(
                user_data["data"]["email"])
            if not memberInfoDB:
                return jsonify({"error": True, "message": "舊密碼錯誤"}), 400

            if memberInfoDB["password"] == data["oldPsw"]:
                result = model.db.update_member(
                    user_data["data"]["id"],
                    data["username"],
                    data["email"],
                    data["newPsw"])
                return jsonify({"ok": result, "message": "更新成功"}), 200
            else:
                return jsonify({"error": True, "message": "舊密碼錯誤"}), 400
