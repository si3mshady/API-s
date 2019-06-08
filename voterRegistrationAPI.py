from flask import Flask, request
from flask_restful import Resource,Api
from pymongo import MongoClient as EMCEE
import  bcrypt

app=application=Flask(__name__)
api=Api(app)
#connect to mongoDB
cursor = EMCEE("mongodb://voting_database:27017")
db = cursor['D4llas_Runoff']
current_collection = db["runoff"]

class Register(Resource):
    def post(self):
        '''Register the voter'''
        data = request.get_json()
        username = data['username']
        password = data['password']
        #hash password - store it in the 'base
        hashed_pw = bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt())
        current_collection.insert({
            "username":username,
            "hashed_pass":hashed_pw,
             "tokens": 1}
        )
        json_response = {
            "status": 200,
            "message": f"Thank you for registering to vote, {username}!"
        }
        return json_response

class Vote(Resource):
    def post(self):
        '''parse response for proper params'''
        data = request.get_json()
        username = data['username']
        password = data['password']
        candidate = data['candidate']

        '''verify password hash matches hash from db'''
        try:
            '''retrieve hashed pw from db'''
            hashed_pw = current_collection.find({"username": username})[0]['hashed_pass']
            if bcrypt.hashpw(password.encode('utf8'), hashed_pw) != hashed_pw:
                json_response = {
                "status": 301,
                "message": f"Incorrect password for, {username}!"
                }
                return json_response
            '''verify if user has voted, expending a token'''
            if current_collection.find({"username":username})[0]['tokens'] != 1:
                 json_response = {
                    "status": 303,
                    "message":  f"User {username}, has already voted."
                }
                 return json_response
        except IndexError:
            json_response = {
                "status": 302,
                "message": f"User {username} does not exist. Please register to vote."
            }
            return json_response
        '''update collection'''
        current_collection.update({"username":username}, { "$set": { "tokens": 0,"voted for" : candidate} })
        json_response = {
            "status": 200,
            "message": f"Thank you for voting, {username}!"
        }
        return json_response

api.add_resource(Register,'/register')
api.add_resource(Vote,'/vote')

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)

#api practice with Docker containers, flask, pymongo and flask-restful. Created a simple API for registering voters - D4llas Run-off
#Elliott Arnold = si3mshady 6-8-19
















