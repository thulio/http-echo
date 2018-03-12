import os

from flask import Flask, jsonify, request, json
from flask_pymongo import PyMongo

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/http_echo")

DEFAULT_METHODS = ["GET", "POST"]

app = Flask(__name__)
app.config["MONGO_URI"] = MONGO_URI
mongo = PyMongo(app)


@app.route("/echo", methods=DEFAULT_METHODS)
def echo():
    args = request.args or {}
    body = request.get_json() or {}

    mongo.db.requests.insert({"args": args, "body": body})

    return jsonify(dict(ok=True, args=args, body=body))


if __name__ == "__main__":
    app.run(port=os.getenv("PORT", 5000), debug=os.getenv("DEBUG", "0") == "1")
