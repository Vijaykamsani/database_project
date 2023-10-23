from flask import Flask, Response, request
import pymongo
import json
from bson.objectid import ObjectId

app = Flask(__name__)


try:
    mongo = pymongo.MongoClient(
        host="localhost",
        port=27017,
        serverSelectionTimeoutMS=3000
    )
    db = mongo.database
    mongo.server_info()
except:
    print("Error - Cannot connect to DB")


@app.route('/api', methods=['POST'])
def add():
    try:
        data = {
            "id": int(request.form["id"]),
            "title": request.form["title"],
            "clips_count": int(request.form["clips_count"]),
            "description": request.form["description"],
            "episodes_count": int(request.form["episodes_count"]),
            "genres": str(request.form["genres"].split(",")),
            "score": float(request.form["score"]),
            "seasons_count": int(request.form["seasons_count"]),
            "company": request.form["company"],
            "rating": request.form["rating"]
        }

        res = db.hulu.insert_one(data)

        return Response(
            response=json.dumps(
                {
                    "message": "Movies and shows inserted successfully",
                    "_id": f"{res.inserted_id}"
                }
            ),
            status=200,
            mimetype="application/json"
        )
    except Exception as ex:
        return Response(
            response=json.dumps(
                {
                    "message": "Film insertion failed"
                }
            ),
            status=500,
            mimetype="application/json"
        )


@app.route('/api/<string:fname>', methods=['PATCH'])
def update(fname):
    try:
        data = {
            "id": int(request.form["id"]),
            "title": request.form["title"],
            "description": request.form["description"],
            "score": float(request.form["score"]),
            "rating": request.form["rating"]
        }

        res = db.hulu.update_one(
            {"title": fname},
            {"$set": data}
        )

        if res.modified_count == 1:
            return Response(
                response=json.dumps(
                    {
                        "message": "Movie and show updated successfully"
                    }
                ),
                status=200,
                mimetype="application/json"
            )
        else:
            return Response(
                response=json.dumps(
                    {
                        "message": "No changes made"
                    }
                ),
                status=200,
                mimetype="application/json"
            )
    except Exception as ex:
        return Response(
            response=json.dumps(
                {
                    "message": "Movie and show updation failed"
                }
            ),
            status=500,
            mimetype="application/json"
        )


@app.route('/api/<string:fname>', methods=['DELETE'])
def delete(fname):
    try:
        res = db.hulu.delete_one({"title": fname})

        if res.deleted_count == 1:
            return Response(
                response=json.dumps(
                    {
                        "message": "Movie and show deleted successfully"
                    }
                ),
                status=200,
                mimetype="application/json"
            )

        return Response(
            response=json.dumps(
                {
                    "message": "Movie and show not found"
                }
            ),
            status=200,
            mimetype="application/json"
        )
    except Exception as ex:
        return Response(
            response=json.dumps(
                {
                    "message": "Movie and show updation failed"
                }
            ),
            status=500,
            mimetype="application/json"
        )


@app.route('/api', methods=['GET'])
def getAll():
    try:
        data = list(db.hulu.find())
        for res in data:
            res["_id"] = str(res["_id"])

        return Response(
            response=json.dumps(data),
            status=200,
            mimetype="application/json"
        )
    except Exception as ex:
        return Response(
            response=json.dumps(
                {
                    "message": "Get Movie and show details failed"
                }
            ),
            status=500,
            mimetype="application/json"
        )


@app.route('/api/<string:fname>', methods=['GET'])
def getByTitle(fname):
    try:
        data = db.hulu.find_one({"title": fname})
        data["_id"] = str(data["_id"])

        return Response(
            response=json.dumps(data),
            status=200,
            mimetype="application/json"
        )
    except Exception as ex:
        print(ex)
        return Response(
            response=json.dumps(
                {
                    "message": "Cannot get Movie and show details"
                }
            ),
            status=500,
            mimetype="application/json"
        )


if __name__ == "__main__":
    app.run(host="localhost", port=5000, debug=True)
