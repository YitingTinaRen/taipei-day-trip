from flask import *
import model

attraction_api = Blueprint('attraction_api', __name__)

@attraction_api.route("/api/attractions", methods=['GET'])
def api_attraction():
	# Get parameters
	page=request.args.get('page',0)
	keyword=request.args.get('keyword')
	result = model.attraction.load_attractions(page, keyword)
	return result

    

@attraction_api.route("/api/attraction/<attractionId>")
def api_attractionId(attractionId):
	attractionId=int(attractionId)
	result=model.attraction.load_by_id(attractionId)
	return result


@attraction_api.route("/api/categories", methods=["GET"])
def api_categories():
	result=model.attraction.load_categories()
	return result
