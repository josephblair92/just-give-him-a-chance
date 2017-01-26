from flask import Flask, request, jsonify, abort
from pymongo import MongoClient
import os
import datetime

app=Flask(__name__, static_url_path='')

@app.route('/')
def root():
	return "Hello World"

if __name__ == '__main__':
	port = int(os.environ.get('PORT', 5000))
	app.run(host='0.0.0.0', port=port)