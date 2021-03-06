from flask import Flask, request, jsonify, abort, Response
from pymongo import MongoClient
import os
import datetime
import json
from bson import ObjectId

class JSONEncoder(json.JSONEncoder):
	def default(self, o):
		if isinstance(o, ObjectId):
			return str(o)
		return json.JSONEncoder.default(self, o)


def init_mongo():
	
	#uri='mongodb://%s:%s@%s:%s/%s' % (mongo_username, mongo_password, mongo_host, mongo_port, mongo_dbname)

	mongo_dbname='justgivehimachance'
	uri=os.environ['JGHAC_MONGO_URI']
	mongo_client=MongoClient(uri)

	global db
	db=mongo_client[mongo_dbname]

app=Flask(__name__, static_url_path='')
init_mongo()

@app.route('/')
def root():
	return "Hello World"

@app.route('/actions')
def get_actions():
	filters=list()
	#process each query param and add filter
	if "categories" in request.args:
		filters.append(get_categories_filter(request.args.getlist("categories")))
	#put all filters into $and, or match all if filter list is empty
	if len(filters) > 0:
		query = {"$and": filters}
	else:
		query = {}
	#execute query and return
	data=list(db["actions"].find(query))
	return Response(JSONEncoder().encode(data), mimetype="application/json")

def get_categories_filter(categories):
	#lowercase the list to avoid case sensitivity problems
	categories = [x.lower() for x in categories]
	return {"categories": {"$in": categories}}

@app.route('/actions/<action_id>')
def get_action(action_id):
	action = db["actions"].find_one({"_id":ObjectId(action_id)})
	action["_id"] = str(action["_id"])
	return jsonify(action)

@app.route('/categories')
def get_categories():
	data=list(db["categories"].find({}))
	return Response(JSONEncoder().encode(data), mimetype="application/json")


if __name__ == '__main__':
	port = int(os.environ.get('PORT', 5000))
	app.run(host='0.0.0.0', port=port)