import os

from flask import Flask, jsonify, request, json
from flask_pymongo import PyMongo

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/http_echo")

ALL_METHODS = ['GET', 'HEAD', 'POST', 'PUT', 'DELETE', 'OPTIONS']

app = Flask(__name__)
app.config["MONGO_URI"] = MONGO_URI
mongo = PyMongo(app)


@app.route('/', defaults={'path': ''}, methods=ALL_METHODS)
@app.route('/<path:path>', methods=ALL_METHODS)
def echo(path):
    args = request.args or {}
    form = request.form
    json_ = request.get_json()
    method = request.method
    headers = dict(request.headers)
    data = request.data.decode("utf-8") if not json_ else None
    remote = dict(
        address=request.environ["REMOTE_ADDR"],
        port=request.environ["REMOTE_PORT"])
    content_type = request.content_type

    mongo_payload = dict(
        args=args,
        form=form,
        json=json_,
        data=data,
        method=method,
        path=path,
        headers=headers,
        remote=remote,
        content_type=content_type)

    mongo.db.requests.insert(mongo_payload)
    mongo_payload.pop("_id")

    return jsonify(dict(ok=True, **mongo_payload))


if __name__ == "__main__":
    app.run(
        port=int(os.getenv("PORT", 5000)),
        debug=os.getenv("DEBUG", "0") == "1")
