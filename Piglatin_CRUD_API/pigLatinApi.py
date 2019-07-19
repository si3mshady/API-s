from flask import Flask, request, jsonify
from flask_restful import Resource,Api
from flask_jwt_simple import  JWTManager, jwt_required, create_jwt
from pigLatin import evaluate
from database import (insert_rds,delete_record,dropTable,fetchAllTranslations,update_email_rds,
                        register,validate_username_password, check_username_exist)


app=application=Flask(__name__)
api=Api(app)

app.config['JWT_SECRET_KEY'] = 'si3mshady'

jwt = JWTManager(app)

class Register(Resource):
    def post(self):
        if not request.is_json:
            return jsonify({"msg": "Missing JSON in request"}), 400
        data = request.get_json()
        username = data['username']
        password = data['password']
        if check_username_exist(username):
            return jsonify({"msg": "Username exists, please choose a new username"}), 400
        register(username,password)
        json_response = {
            "status": 200,
            "msg": f"Thank you for registering {username}"
        }

        return jsonify(json_response)

class Login(Resource):
    def post(self):
        if not request.is_json:
            return jsonify({"msg": "Missing JSON in request"}), 400
        data = request.get_json()
        username = data['username']
        password = data['password']
        if not validate_username_password(username,password):
            return jsonify({"msg": "Username or Password is invalid!"}), 400
        json_response = {
            "status": 200,
            "jwt": create_jwt(identity=username)
        }
        return json_response


class Translate_Pig_Latin(Resource):
    @jwt_required
    def post(self):
        if not request.is_json:
            return jsonify({"msg": "Missing JSON in request"}), 400
        data = request.get_json()
        email = data['email']
        word = data['word']
        translated = evaluate(word)
        insert_rds(email,word,translated)
        json_response = {
            "status": 200,
            "msg":  f"{word} equals {translated}"
        }
        return json_response

class Update_Email(Resource):
    @jwt_required
    def put(self):
        if not request.is_json:
            return jsonify({"msg": "Missing JSON in request"}), 400
        data = request.get_json()
        old_email = data['old_email']
        new_email = data['new_email']
        update_email_rds(old_email,new_email)
        json_response = {
            "status": 200,
            "msg": f"Old Email {old_email} has been replaced with {new_email}!"
        }

        return json_response


class DeleteRecord(Resource):
    @jwt_required
    def delete(self):
        if not request.is_json:
            return jsonify({"msg": "Missing JSON in request"}), 400
        data = request.get_json()
        email = data['email']
        delete_record(email)
        json_response = {
            "status": 200,
            "msg": "Record deleted!"
        }
        return json_response

class DropTable(Resource):
    @jwt_required
    def post(self):
        if not request.is_json:
            return jsonify({"msg": "Missing JSON in request"}), 400
        data = request.get_json()
        table = data['tablename']
        dropTable(table)
        json_response = {
            "status": 200,
            "msg": f"Table {table} Deleted"
        }
        return json_response



class GetTranslations(Resource):
    @jwt_required
    def post(self):
        if not request.is_json:
            return jsonify({"msg": "Missing JSON in request"}), 400
        results = fetchAllTranslations()
        json_response = {
            "status": 200,
            "msg": results
        }
        return json_response



api.add_resource(Register,'/register')
api.add_resource(Login,'/login')
api.add_resource(Translate_Pig_Latin,'/translation')
api.add_resource(Update_Email,'/update_email')
api.add_resource(DeleteRecord,'/delete_record')
api.add_resource(DropTable,'/drop_table')
api.add_resource(GetTranslations,'/fetch_all')

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')

#AWS/FLASK/RDS/CRUD practice - API that returns pig latin translation of the input
#Data is written to RDS tables in AWS
#Elliott Arnold  7-19-19
#si3mshady













