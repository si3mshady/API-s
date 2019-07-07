from flask import Flask, request, jsonify
from flask_restful import Resource,Api
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_simple import  JWTManager, jwt_required, create_jwt
import subprocess
from pathlib import Path
from pymongo import MongoClient

app=application=Flask(__name__)
api=Api(app)

app.config['JWT_SECRET_KEY'] = 'si3mshady'
#connect to mongoDB
cursor = MongoClient("mongodb://localhost:27017")
db = cursor['filesystem']
current_collection = db["fs"]
jwt = JWTManager(app)

def username_exist(username):
    if current_collection.find_one({"username":username}):
        return True
def get_password_hash(username):
    hp = current_collection.find_one({"username": username})["hashed_pass"]
    return hp

class Login(Resource):
    def post(self):
        if not request.is_json:
            return jsonify({"msg": "Missing JSON in request"}), 400
        data = request.get_json()
        username = data['username']
        password = data['password']
        hp = get_password_hash(username)
        if not username_exist(username):
            return jsonify({"msg": "Username does not exist"}), 400
        if not check_password_hash(hp,password):
            return jsonify({"msg": "Incorrect Password"}), 400
        json_response = {
            "status": 200,
            "jwt": create_jwt(identity=username)
        }
        return json_response

class Register(Resource):
    def post(self):
        data = request.get_json()
        username = data['username']
        password = data['password']
        #hash password - store it in the 'base
        hashed_pw = generate_password_hash(password)
        current_collection.insert({"username":username,"hashed_pass":hashed_pw})
        json_response = {
            "status": 200,
            "message": f"Thank you for registering, {username}!"
        }
        return json_response

class GetFileCount(Resource):
    @jwt_required
    def post(self):
        data = request.get_json()
        path = data['path']
        fullpath = str(Path(path))
        print(fullpath)
        cmd = 'ls ' + fullpath
        data = subprocess.Popen(cmd, stdout=subprocess.PIPE,shell=True)
        out, err = data.communicate()
        out = out.decode()
        out = out.split('\n')
        json_response = {
            "status": 200,
            "file count": len(out)
        }
        return json_response

api.add_resource(Register,'/register')
api.add_resource(GetFileCount,'/count')
api.add_resource(Login,'/login')

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)


#API practice - created a simple API that uses JWT for authentication - Registration and Login required to view file count of a directory
#Elliott Arnold 7-7-19 = si3mshady
#https://flask-jwt-extended.readthedocs.io/en/latest/basic_usage.html