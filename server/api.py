from flask import Blueprint, jsonify
from flask_cors import CORS

api = Blueprint("api", __name__)

CORS(api)

@api.route('/api/hello')
def say_hello():
    return jsonify("hello")

