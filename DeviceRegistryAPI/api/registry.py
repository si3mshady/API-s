from flask import Flask, jsonify, request
from flask_restful import Resource,Api
from pymongo import MongoClient, errors
from datetime import datetime
import redis, pymongo

'''connect to mongodb container'''
cursor = MongoClient('mongodb://mongo-service:27017')
db = cursor['device_registry']
current_collection = db['registry']

'''connect to redis container'''
redis_client = redis.Redis(host='redis-service', port=6379, db=0)

'''create app and wrap in in flask-restful'''
app=application=Flask(__name__)
api=Api(app)

'''CRUD methods'''
def genDateString():
    now = datetime.now()
    dateString = now.strftime("%b-%d-%Y %H:%M:%S")
    return dateString


def get_all_devices():
    registered = current_collection.find()
    devices = list(registered)
    return devices

def get_device(identifier):
    data = current_collection.find({"_id": identifier})
    device = list(data)[0]
    return device

def delete_document(deviceValue):
    item = {"_id": deviceValue}
    if current_collection.delete_one(item):
        return True

def insert_db(identifier, name, device_type, controller_gateway):
    '''override default '_id' key as it's value not json serializable - ObjectId '''
    current_collection.insert({
        "_id": identifier,
        "name": name,
        "device_type": device_type,
        "device_controller" : controller_gateway
    })

'''GET & POST methods to view all devices and register new ones'''
class Devices(Resource):
    def get(self):
        devices = get_all_devices()
        return jsonify(data='200',message=devices)

    def post(self):
        try:
            '''retrieve data from response insert data into redis and mongodb - return json response'''
            data = request.get_json()
            identifier = data['_id']
            name = data['name']
            device_type = data['device_type']
            device_controller = data['device_controller']
            redis_client.set(f'insert-timestamp-{identifier}', genDateString())
            insert_db(identifier, name, device_type, device_controller)
            return jsonify(data='201', message=f"{name.title()} has been added to device registry.")
        except pymongo.errors.DuplicateKeyError:
            return jsonify(data='400', message="Duplicate Key Error")
        except KeyError:
            return jsonify(data='400', message="Key Error")

'''GET & DELETE methods to view single device or delete device from database'''
class Device(Resource):
    def get(self, identifier):
        device = get_device(identifier)
        date_added = redis_client.get(f'insert-timestamp-{identifier}')
        device['date-added'] = date_added.decode()
        return jsonify(data='200',message=device)

    def delete(self, identifier):
        if delete_document(identifier):
            return jsonify(data="204",message=f"{identifier.title()} has been deleted from registry.")
        else:
            return jsonify(data="404", message=f"{identifier.title()} is not found (404).")

'''create endpoints'''
api.add_resource(Devices,'/devices')
api.add_resource(Device,'/device/<identifier>')

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)

#API/Docker/Kubernetes/Deployment practice
#Device registry api for home automation
#Elliott Arnold 9-22-19










