import mysql.connector
from flask import *

app=Flask(__name__)
app.config["JSON_AS_ASCII"]=False
app.config["TEMPLATES_AUTO_RELOAD"]=True


def checkData(sql, val=()):
	# return data type is dictionary
	mydb=mysql.connector.connect(pool_name="mypool")
	mycursor=mydb.cursor(dictionary=True)
	mycursor.execute(sql, val)
	myresult=mycursor.fetchall()
	mycursor.close()
	mydb.close()
	return myresult


def split_chunks(list, itemNo_chunk):
	# How many elements each
	# list should have itemNo_chunk
	
	# using list comprehension
	result = [list[i * itemNo_chunk:(i + 1) * itemNo_chunk] for i in range((len(list) + itemNo_chunk - 1) // itemNo_chunk )]
	final={}
	for n in range(len(result)):
		if n == len(result)-1:
			final[n]=dict(Data=result[n], nextPage=None)
		else:
			final[n]=dict(Data=result[n], nextPage=n+1)
	
	# select_img="select images from imgURL where id =%s"
	# val=(result[n])

	return final

def list_dict2value_list(lsts, key):
  return [x.get(key) for x in lsts]

def urls(list):
	# put image urls into attraction list
	for i in range(len(list)):
		sql="select images from imgURL where id= %s and (lower(images) like '%jpg' or lower(images) like '%jpeg' or lower(images) like '%png')"
		val=(list[i]["id"],)
		imgs=checkData(sql, val)
		imgs=list_dict2value_list(imgs, "images")
		list[i].update({"images":imgs})
	
	return list

# Pages
@app.route("/")
def index():
	return render_template("index.html")
@app.route("/attraction/<id>")
def attraction(id):
	return render_template("attraction.html")
@app.route("/booking")
def booking():
	return render_template("booking.html")
@app.route("/thankyou")
def thankyou():
	return render_template("thankyou.html")

@app.route("/api/attractions", methods=['GET'])
def api_attraction():
	# Get parameters
	page=request.args.get('page',0)
	keyword=request.args.get('keyword')
	page=int(page)
	
	# number of items in one page
	NumInOnePage=12

	print(keyword)
	# Check if there is keyword?
	if keyword: # There is keyword
		print("there is keyword")
		ambig_keyword='%'+keyword+'%'
		print(ambig_keyword)
		sql="select id, name, category, description, address, transport, mrt, lat, lng from attractions "\
			"where (category= %s or description like %s)"
		val=(keyword, ambig_keyword,)
		attractions=checkData(sql, val)
		if not attractions: return jsonify({"error": True, "message": "Empty search, change keyword or do not use keyword."}), 500

		# put image urls into attraction list
		attractions= urls(attractions)

		# split attractions every 12 items
		attractions=split_chunks(attractions, NumInOnePage)
	else: # There is no keyword
		print("there is no keyword")
		sql="select id, name, category, description, address, transport, mrt, lat, lng from attractions "
		attractions=checkData(sql)
		if not attractions: return jsonify({"error": True, "message": "Something wrong on server side."}), 500
		
		# put image urls into attraction list
		attractions= urls(attractions)


		# split attractions every 12 items
		attractions=split_chunks(attractions, NumInOnePage)


	if page > len(attractions)-1:
		return jsonify({"error": True, "message": "Max page is "+str(len(attractions)-1)}), 500
	else:
		return jsonify(attractions[page]), 200

@app.route("/api/attraction/<attractionId>")
def api_attractionId(attractionId):
	attractionId=int(attractionId)

	sql="select id, name, category, description, address, transport, mrt, lat, lng from attractions where id = %s"
	val=(attractionId,)

	try:
		attractions=checkData(sql, val)
		if not attractions: return jsonify({"error": True, "message": "ID does not exist."}), 400
	except:
		return jsonify({"error":True, "message":"Server internal error."}), 500
		
	# put image urls into attraction list
	attractions= urls(attractions)

	return jsonify(attractions), 200

@app.route("/api/categories", methods=["GET"])
def api_categories():
	
	sql="select category from attractions"
	
	try:
		attractions=checkData(sql)
	except:
		return jsonify({"error":True, "message":"Server internal error."}), 500
	
	list = list_dict2value_list(attractions, "category")
	print(list)

	return jsonify({"data":list}), 200


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
app.run(host='0.0.0.0', port=3000)