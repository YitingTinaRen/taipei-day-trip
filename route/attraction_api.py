from flask import *
import mysql.connector

attraction_api = Blueprint('attraction_api', __name__)

def checkData(sql, val=()):
	# return data type is dictionary
	mydb=mysql.connector.connect(pool_name="mypool")
	mycursor=mydb.cursor(dictionary=True)
	mycursor.execute(sql, val)
	myresult=mycursor.fetchall()
	mycursor.close()
	mydb.close()
	return myresult

def list_dict2value_list(lsts, key):
  return [x.get(key) for x in lsts]

def urls(list):
    # put image urls into attraction list
	for i in range(len(list)):
		sql="select images from imgURL where id= %s and (lower(images) like '%jpg' or lower(images) like '%jpeg' or lower(images) like '%png')"
		# sql="select images from imgURL where id= %s"
		val=(list[i]["id"],)
		imgs=checkData(sql, val)
		imgs=list_dict2value_list(imgs, "images")
		list[i].update({"images":imgs})
	
	return list

@attraction_api.route("/api/attractions", methods=['GET'])
def api_attraction():
	# Get parameters
	page=request.args.get('page',0)
	keyword=request.args.get('keyword')
	page=int(page)
	
	# number of items in one page
	NumInOnePage=12

	# Check if there is keyword?
	if keyword: # There is keyword
		ambig_keyword='%'+keyword+'%'
		sql="select id, name, category, description, address, transport, mrt, lat, lng from attractions "\
			"where (category= %s or name like %s) "\
			"order by id asc "\
			"limit %s, %s"
		val=(keyword, ambig_keyword, page*NumInOnePage, NumInOnePage+1,) # request 1 more data than the requested to see if we will have next page
	else: # There is no keyword
		sql="select id, name, category, description, address, transport, mrt, lat, lng from attractions order by id asc limit %s, %s "
		val=(page*NumInOnePage, NumInOnePage+1,)
	
	# Search in mysql
	try:
		attractions=checkData(sql, val)
		if  len(attractions) ==0: # if serch result is empty
			return jsonify({"error": True, "message": "Empty result."}), 500
	except mysql.connector.Error as err:
		print(err) #print mysql error
		return jsonify({"error": True, "message": "Server internal error."}), 500
		
	# put image urls into attraction list
	attractions= urls(attractions)
	print(len(attractions))
	# Return results
	if len(attractions) == NumInOnePage+1: # check if there will be at least one more data in the next page
		return jsonify(dict(data=attractions[0:NumInOnePage], nextPage=page+1)), 200
		
	else:
		return jsonify(dict(data=attractions[0:NumInOnePage], nextPage=None)),200
    

@attraction_api.route("/api/attraction/<attractionId>")
def api_attractionId(attractionId):
	attractionId=int(attractionId)

	sql="select id, name, category, description, address, transport, mrt, lat, lng from attractions where id = %s"
	val=(attractionId,)

	try:
		attractions=checkData(sql, val)
		if len(attractions) ==0: return jsonify({"error": True, "message": "ID does not exist."}), 400 # if serch result is empty
	except mysql.connector.Error as err:
		print(err) #print mysql error
		return jsonify({"error":True, "message":"Server internal error."}), 500
		
	# put image urls into attraction list
	attractions= urls(attractions)
	attractions=dict(data=attractions[0])

	return jsonify(attractions), 200

@attraction_api.route("/api/categories", methods=["GET"])
def api_categories():
	
	sql="select distinct category from attractions"
	
	try:
		attractions=checkData(sql)
	except mysql.connector.Error as err:
		print(err) #print mysql error
		return jsonify({"error":True, "message":"Server internal error."}), 500 
	
	list = list_dict2value_list(attractions, "category")

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