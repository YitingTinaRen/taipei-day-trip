from flask import *
import model.user as user


account_api = Blueprint('account_api', __name__)


@account_api.route("/api/user", methods=["POST"])
def register():
    user_data=request.get_json()
    username=user_data["name"]
    email=user_data["email"]
    psw=user_data["password"]
    
    result= user.USER.register(username,email,psw)
    return result
    
@account_api.route("/api/user/auth", methods=["GET", "PUT", "DELETE"])
def auth():
    if request.method=="PUT":
        user_data=request.get_json()
        email=user_data["email"]
        password=user_data["password"]

        result=user.USER.login(email, password)
        return result
    elif request.method=="GET":
        token=request.cookies.get("user")
        result=user.USER.auth(token)
        return result
    elif request.method=="DELETE":
        result=user.USER.delete_token()
        return result


