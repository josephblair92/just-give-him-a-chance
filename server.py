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
	data=list(db["actions"].find({}))
	print(data)
	return Response(JSONEncoder().encode(data), mimetype="application/json")

@app.route('/categories')
def get_categories():
	data=list(db["categories"].find({}))
	return Response(JSONEncoder().encode(data), mimetype="application/json")


if __name__ == '__main__':
	port = int(os.environ.get('PORT', 5000))
	app.run(host='0.0.0.0', port=port)