from flask import *
import model
import os
from PIL import Image

member_api = Blueprint('member_api', __name__)


@member_api.route("api/member", methods=["POST", "DELETE"])
def member():
    if request.method=="POST":
        token = request.cookies.get("user")
        result=model.orders.check_order(token)
        return result
    else:
        token = request.cookies.get("user")
        order_num = request.get_json("order_num")
        result = model.orders.delete_order(token, order_num)
        return result

@member_api.route("api/memberPic",methods=["POST", "GET"])
def memberPic():
    if request.method =="POST":
        token = request.cookies.get("user")
        token_info = model.USER.auth(token)
        token_info = json.loads(token_info[0].data)

        file = request.files["userPic"]
        current_path = os.getcwd()
        image_path = current_path+"/static/imgs/userPic/" + \
            str(token_info["data"]["id"])+".png"
        image_path_relative = "/static/imgs/userPic/" + \
            str(token_info["data"]["id"])+".png"

        result = model.db.uploadUserPic(token_info["data"]["id"], image_path_relative)
        file.save(image_path)
        if result:
            return jsonify({"ok":True}), 200
        else:
            return jsonify({"error":True, "message":"server error."}), 500
    
    elif request.method=="GET":
        token = request.cookies.get("user")
        token_info = model.USER.auth(token)
        token_info = json.loads(token_info[0].data)

        result = model.db.loadUserPic(token_info["data"]["id"])
        if result:
            return jsonify({"ok":True, "url":result["pic_path"]}), 200
        else:
            return jsonify({"ok":True, "url":None}), 200
