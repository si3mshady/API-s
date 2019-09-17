from flask import Flask, request
from flask_restful import Resource, Api
from pymongo import MongoClient

app = application = Flask(__name__)
api = Api(app)

cursor = MongoClient('mongodb://mongo:27017')
db = cursor['k8']
current_collection = db['current']


def insert_db(username,email):
    current_collection.insert({
        "username": username,
        "email": email
    })

def count():
    registered = current_collection.find({}).count()
    return registered

class Register(Resource):
    def post(self):
        try:
            data = request.get_json()
            user = data['username']
            email = data['email']

            insert_db(user,email)
            json_response = {
                "status": 200,
                "message": f"Thank you for registering {user}!"
            }
            return json_response
        except KeyError:
            json_response = {
                "status": 300,
                "message": "Key Error"
            }
            return json_response

class Registered(Resource):
    def get(self):
        registered = count()
        if registered is None:
            registered = 0
        json_response = {
            "status": 200,
            "message": f" {registered} accounts registered!"
        }
        return json_response


api.add_resource(Register, '/register')
api.add_resource(Registered, '/count')

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)


#Elliott Arnold 9-16-19  K8 practice deploying a small api