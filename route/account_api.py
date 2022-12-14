from flask import *
import model


account_api = Blueprint('account_api', __name__)


@account_api.route("/api/user", methods=["POST", "PATCH"])
def register():
    if request.method=="POST":
        user_data = request.get_json()
        username = user_data["name"]
        email = user_data["email"]
        psw = user_data["password"]
        result= model.USER.register(username,email,psw)
        return result
    elif request.method=="PATCH":
        token = request.cookies.get("user")
        user_data = request.get_json()
        result=model.USER.update_user_info(user_data,token)
        return result
    
@account_api.route("/api/user/auth", methods=["GET", "PUT", "DELETE"])
def auth():
    if request.method=="PUT":
        user_data=request.get_json()
        email=user_data["email"]
        password=user_data["password"]

        result=model.USER.login(email, password)
        return result
    elif request.method=="GET":
        token=request.cookies.get("user")
        result=model.USER.auth(token)
        return result
    elif request.method=="DELETE":
        result=model.USER.delete_token()
        return result


