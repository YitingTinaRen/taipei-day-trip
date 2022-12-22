import model
from flask import jsonify

NumInOnePage=12
class attraction:
    

    def list_dict2value_list(lsts, key):
        return [x.get(key) for x in lsts]

    def urls(list):
        # put image urls into attraction list
        for i in range(len(list)):
            imgs=model.db.search_image_by_id(list[i]["id"])
            imgs=attraction.list_dict2value_list(imgs, "images")
            list[i].update({"images":imgs})
	
        return list
    
    def load_attractions(page, keyword):
        page=int(page)
        # Search in mysql
        try:
            if keyword:
                attractions=model.db.search_by_keyword(keyword,page, NumInOnePage)
            else:
                attractions=model.db.search_by_page(page,NumInOnePage)
            
            # attractions=checkData(sql, val)
            if  len(attractions) ==0: # if serch result is empty
                return jsonify({"error": True, "message": "Empty result."}), 500
        except:
            return jsonify({"error": True, "message": "Server internal error."}), 500
            
        # put image urls into attraction list
        attractions= attraction.urls(attractions)
        print(len(attractions))
        # Return results
        if len(attractions) == NumInOnePage+1: # check if there will be at least one more data in the next page
            return jsonify(dict(data=attractions[0:NumInOnePage], nextPage=page+1)), 200
            
        else:
            return jsonify(dict(data=attractions[0:NumInOnePage], nextPage=None)),200

    def load_by_id(attractionId):
        try:
            attractions=model.db.search_by_id(attractionId)
            if len(attractions) ==0: return jsonify({"error": True, "message": "ID does not exist."}), 400 # if serch result is empty
        except:
            return jsonify({"error":True, "message":"Server internal error."}), 500
            
        # put image urls into attraction list
        attractions= attraction.urls(attractions)
        attractions=dict(data=attractions[0])

        return jsonify(attractions), 200

    def load_categories():
        try:
            attractions=model.db.search_catogories()
        except:
            return jsonify({"error":True, "message":"Server internal error."}), 500 
        
        list = attraction.list_dict2value_list(attractions, "category")

        return jsonify({"data":list}), 200

        