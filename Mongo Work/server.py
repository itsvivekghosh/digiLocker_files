from flask import Flask, Response, request
from bson.objectid import ObjectId
import pymongo
import warnings
import json

###########################
app = Flask(__name__)

try:
    client = pymongo.MongoClient(host='localhost',
                                 port=27017,
                                 serverSelectionTimeoutMS=100)
    db = client['company']  ### Database Name
    client.server_info()  # trigger the exception if not connected to db
except:
    print("ERROR - Cannot connect to db")


####################################
@app.route('/users', methods=['POST'])
def create_user():
    try:
        user = {
            'name': request.form['name'],
            "company": request.form['company']
        }
        dbResponse = db['users'].insert_one(user)
        response = {
            'message': "user created",
            "id": f"{dbResponse.inserted_id}"
        }
        return Response(json.dumps(response),
                        status=200,
                        mimetype="application/json")
    except Exception as ex:
        print("********************************")
        print(ex)
        print("********************************")


@app.route('/users', methods=["GET"])
def get_users():
    try:
        data = list(db.users.find())
        for user in data:
            user['_id'] = str(user['_id'])
        return Response(response=json.dumps(data),
                        status=200,
                        mimetype="application/json")
    except Exception as ex:
        print("********************************")
        print(ex)
        print("********************************")
        response = {
            'message': "cannot read users created",
        }
        return Response(json.dumps(response),
                        status=500,
                        mimetype="application/json")


@app.route('/users/<id>', methods=["PATCH"])
def update_user(id):
    try:
        dbResponse = db['users'].update_one(
            {"_id": ObjectId(id)}, {"$set": {
                "name": request.form['name']
            }})

        if dbResponse.modified_count >= 1:
            message = "user updated successfully"
        else:
            message = "nothing updated"

        response = {
            'message': message,
        }
        return Response(json.dumps(response),
                        status=200,
                        mimetype="application/json")
    except Exception as ex:
        print("********************************")
        print(ex)
        print("********************************")
        response = {
            'message': "cannot update the current user",
        }
        return Response(json.dumps(response),
                        status=500,
                        mimetype="application/json")


@app.route("/users/<id>", methods=["DELETE"])
def delete_user(id):
    try:
        dbResponse = db['users'].delete_one({"_id": ObjectId(id)})
        # for attr in dir(dbResponse):
        #     print(attr)
        if dbResponse.deleted_count >= 1:
            message = "user deleted"
        else:
            message = "No user was deleted!"
        response = {'message': message, 'id': f"{id}"}
        return Response(json.dumps(response),
                        status=500,
                        mimetype="application/json")
    except Exception as ex:
        print("********************************")
        print(ex)
        print("********************************")
        response = {'message': "cannot delete user", 'id': f"{id}"}
        return Response(json.dumps(response),
                        status=500,
                        mimetype="application/json")


###########################
if __name__ == '__main__':
    app.run(port=80, debug=True)