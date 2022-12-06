from flask import *
import mysql.connector
import re
import jwt
from functools import wraps
from datetime import datetime, timedelta
from flask import current_app as app


jwt_algo="HS256"

account_api = Blueprint('account_api', __name__)

def check_for_token(func):
    @wraps(func)
    def wrapped(*args, **kwargs):
        token=request.cookies
        print(token)
        print(bool(token))
        # Check if there is token
        if not token:
            return jsonify({"data":None}), 200
        
        try:
            data=jwt.decode(token, app.config["SECRET_KEY"])
        except:
            return jsonify({"error":True, "message":"Invalid token"}), 400

        return data
    return wrapped



def checkAllData(sql, val=()):
	# return data type is dictionary
	mydb=mysql.connector.connect(pool_name="mypool")
	mycursor=mydb.cursor(dictionary=True)
	mycursor.execute(sql, val)
	myresult=mycursor.fetchall()
	mycursor.close()
	mydb.close()
	return myresult

def checkOneData(sql, val=()):
	# return data type is dictionary
	mydb=mysql.connector.connect(pool_name="mypool")
	mycursor=mydb.cursor(dictionary=True)
	mycursor.execute(sql, val)
	myresult=mycursor.fetchone()
	mycursor.close()
	mydb.close()
	return myresult

def writeData(sql, val):
    try:
        mydb=mysql.connector.connect(pool_name="mypool")
        mycursor=mydb.cursor()
        mycursor.execute(sql, val)
        mydb.commit()
        mycursor.close()
        mydb.close()
        return True
    except:
        return False

@account_api.route("/api/user", methods=["POST"])
def register():
    user_data=request.get_json()
    print(user_data)
    username=user_data["name"]
    email=user_data["email"]
    psw=user_data["password"]
    
    sql_statement="select * from member where email=%s"
    val=(email,)
    result=checkOneData(sql_statement, val)
    
    if not username or not email or not psw:
        return jsonify({"error":True, "message": "Please fill out the form."}), 400
    elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
        return jsonify({"error":True, "message": "Invalid email."}), 400
    elif result:
        return jsonify({"error": True, "message":"Email already exists."}), 400
    else:
        sql_statement="insert into member (username, email, password) values (%s, %s, %s)"
        val=(username, email, psw,)
        if writeData(sql_statement, val):
            return jsonify({"ok":True}),200
        else:
            return jsonify({"error":True, "message":"Server internal error."}), 500
    
@account_api.route("/api/user/auth", methods=["GET", "PUT", "DELETE"])
def auth():
    print("in auth func")
    if request.method=="PUT":
        user_data=request.get_json()
        email=user_data["email"]
        password=user_data["password"]
        sql="select * from member where email=%s"
        val=(email,)
        DB_result=checkAllData(sql,val)
        if not email or not password:
            return jsonify({"error":True, "message":"Please fill out the form."}), 400

        if not DB_result:
            return jsonify({"error":True, "message":"Email does not exist."}), 400
        elif password == DB_result[0]["password"]:
            # Create JWT token
            token=jwt.encode({
                'userID':DB_result[0]["member_id"],
                'username':DB_result[0]["username"],
                'email':email,
                'exp':datetime.utcnow()+timedelta(minutes=30)
            },
            app.config['SECRET_KEY'], algorithm='HS256')
            print("newly created token:")
            print(token)
            
            # Save to cookie
            res=make_response(jsonify({"ok": True}),200)
            res.set_cookie('user', token)
            return res
        else:
            return jsonify({"error":True, "message":"Wrong password."}), 400
    elif request.method=="GET":
        token=request.cookies.get("user")
        print("Checked token:")
        print(token)
        # Check if there is token
        if not token:
            return jsonify(None), 200
        
        try:
            data=jwt.decode(token, app.config["SECRET_KEY"], algorithms='HS256')
            print(data)
        except jwt.exceptions.InvalidTokenError as error:
            print(error)
            return jsonify({"error":True, "message":"Invalid token"}), 400
        return jsonify({"data":{"id":data["userID"], "name":data["username"],"email":data["email"]}}), 200
    elif request.method=="DELETE":
        res=make_response(jsonify({"ok": True}),200)
        res.delete_cookie('user')
        return res


    return jsonify("in auth func")


# MySQL Database config
dbconfig={
	"host":"localhost",
	"user":"root",
	"password":"0000",
	"database":"TaipeiDayTrip"
}

# Create MySQL pooling
mydb=mysql.connector.connect(
	pool_name="mypool",
	pool_size=20,
	**dbconfig
)
mydb.close()