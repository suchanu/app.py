from flask import Flask, jsonify, request, Response
from pymongo import MongoClient, errors
from bson import ObjectId
from flask_basicauth import BasicAuth

app = Flask(__name__)

app.config['BASIC_AUTH_USERNAME'] = 'login'
app.config['BASIC_AUTH_PASSWORD'] = 'pass'
basic_auth = BasicAuth(app)

client = MongoClient("mongodb+srv://suchanun:suchanun2910@student.ffa9jti.mongodb.net/")
db = client["students"]
students_collection = db["std_info"]

@app.route("/")
def greet():
    return "Welcome to Student Management API"

@app.route("/students", methods=["GET"])
@basic_auth.required
def get_all_students():
    students = students_collection.find()
    return jsonify([student for student in students])

@app.route("/students/<string:_id>", methods=["GET"])
@basic_auth.required
def get_student(_id):
    student = students_collection.find_one({'_id': _id})
    if student:
        return jsonify(student)
    else:
        return jsonify({"error":"Student not found"}), 404

@app.route("/students", methods=["POST"])
@basic_auth.required
def create_student():
    data = request.get_json()
    existing_student = students_collection.find_one({'_id': data['_id']})
    if existing_student:
        return jsonify({"error": "Cannot create new student"}), 500
    result = students_collection.insert_one(data)

    if result.inserted_id:
        student = students_collection.find_one({'_id': data['_id']})
        return jsonify(student), 200

@app.route("/students/<string:_id>", methods=["PUT"])
@basic_auth.required
def update_student(_id):
    data = request.get_json()
    result = students_collection.update_one({'_id': _id}, {'$set': data})
    if result.matched_count:
        student = students_collection.find_one({'_id': _id})
        return jsonify(student), 200
    else:
        return jsonify({"error": "Student not found"}), 404

@app.route("/students/<string:_id>", methods=["DELETE"])
@basic_auth.required
def delete_student(_id):
    result = students_collection.delete_one({'_id': _id})
    if result.deleted_count:
        return jsonify({"message": "Student deleted successfully"}), 200
    else:
        return jsonify({"error": "Student not found"}), 404

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
