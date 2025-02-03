from flask import Flask, jsonify
from flask_cors import CORS
from flask_pymongo import PyMongo

# Initialize the Flask app
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})


# Set the MongoDB URI
app.config["MONGO_URI"] = (
    "mongodb://mongodb:27017/Temp_DB"  # Change this to your DB URI
)

# Initialize the PyMongo object after setting the config
mongo = PyMongo(app)


@app.route("/test-cors")
def test_cors():
    return jsonify({"message": "CORS test"})


@app.after_request
def add_cors_headers(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
    return response
