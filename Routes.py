# https://blog.stoplight.io/python-rest-api
# cpu use multiprocessing & os
# multiprocessing: https://docs.python.org/3/library/multiprocessing.html

from flask import Flask, jsonify

response = {"message": "Hello world"}

# Defining the API

api = Flask(__name__)

# POST request

# @api.route('/', methods=['POST'])
# def index():
#     return 'Hello, World!'

# GET request

@api.route('/companies', methods=['GET'])
def get_companies():
  return jsonify(response)

# Running the API

api.run()
