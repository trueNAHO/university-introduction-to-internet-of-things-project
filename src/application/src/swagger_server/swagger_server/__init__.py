from flask import Flask
from flask_pymongo import PyMongo

# Initialize the Flask app
app = Flask(__name__)

# Set the MongoDB URI
app.config["MONGO_URI"] = "mongodb://localhost:27017/Temp_DB"  # Change this to your DB URI

# Initialize the PyMongo object after setting the config
mongo = PyMongo(app)
