from flask import Flask, request
from flask_restful import Resource,Api
from pymongo import MongoClient
import spacy, boto3, os

'''retrieve env variables from container, set with docker-compose and .env'''
access_key = os.environ.get('ACCESS_KEY')
secret = os.environ.get('SECRET_KEY')

'''initiate flask/flask-restful'''
app=application=Flask(__name__)
api=Api(app)

'''establish connection and cursor with mongodb container '''
cursor = MongoClient('mongodb://mdb:27017')
db = cursor['Text_Similarity']
current_collection = db['current']

'''load natural lan processsing model'''
nlp = spacy.load('en_core_web_sm')

'''create sqs client'''
client = boto3.client('sqs',region_name='us-east-1',
                      aws_access_key_id=access_key,aws_secret_access_key=secret)

'''SQS URLS'''
high_similarity = "https://sqs.us-east-1.amazonaws.com/952151691101/High"
medium_similarity = "https://sqs.us-east-1.amazonaws.com/952151691101/Medium"
low_similarity = "https://sqs.us-east-1.amazonaws.com/952151691101/Low"

'''Comparision String - Test for escalating language'''
escalation_language = "I am experiencing a high severity issue, all systems are down. Please escalate this issue to an engineer immediately!"

def getSimilarity(t1,t2):
    text1 = nlp(t1)
    text2 = nlp(t2)
    ratio = float(text1.similarity(text2) * 100)
    return ratio

def sqs(queue,msg):
    response = client.send_message(QueueUrl=queue, MessageBody=str(msg))

def forward_to_queue(new_issue,ratio):
    if ratio > 69:
        sqs(high_similarity,new_issue)
        return "High similarity"
    elif ratio <= 69 and ratio >= 50:
        sqs(medium_similarity,new_issue)
        return "Medium similarity"
    else:
        sqs(low_similarity,new_issue)
        return "Low similarity"

def insert_db(issue, initial_severity, ratio):
    current_collection.insert({
        "Severity": initial_severity,
        "Issue": issue,
        "Ratio": ratio
    })

class NewIssue(Resource):
    def post(self):
        try:
            data = request.get_json()
            issue = data['new_issue']
            severity = data['severity']
            ratio = getSimilarity(escalation_language, issue)
            response = forward_to_queue(issue,ratio)
            insert_db(issue, severity, ratio)
            json_response = {
                "status": 200,
                "message": response + " Detected.",
                "similarity": ratio
            }
            return json_response
        except KeyError:
            json_response = {
                "status": 300,
                "message": "Key Error"
            }
            return json_response

api.add_resource(NewIssue,'/new')

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)


#Docker, Docker-Compose, Boto3, NLP practice
#A small api which uses NLP (Spacy) to determine the similarity of text messages
#Depending on the similarity, the messages are forwarded to an AWS SQS Queue and written to a NOSQL database
#Elliott Arnold 9-15-19

#https://github.com/explosion/spacy-models
#https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sqs.html#SQS.Client.send_message
#https://blog.agchapman.com/using-variables-in-docker-compose-files/