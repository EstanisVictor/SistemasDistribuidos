#!/usr/bin/env python
# encoding: utf-8
import json
from flask import Flask, request, jsonify
from pymongo import MongoClient
from flask_cors import CORS
from bson.objectid import ObjectId


app = Flask(__name__)
CORS(app)


client = MongoClient("mongodb+srv://estanis:root@cluster0.nsd3vad.mongodb.net/?retryWrites=true&w=majority")
db = client["CRUD-SD"]
users = db["user"]


@app.route("/getAll", methods=["GET"])
def get_all_users():
    output = []
    for q in users.find():
        output.append(
            {"id": str(q.get("_id")), "name": q.get("name"), "email": q.get("email")}
        )
    return jsonify(output)


@app.route("/register", methods=["POST"])
def add_user():
    user = request.get_json()
    print(user)
    users.insert_one(user)
    return jsonify({"result": "User added successfully"})


@app.route("/getUser/<id>", methods=["GET"])
def get_one_user(id):
    print(id)
    try:
        user_id = ObjectId(id)
    except:
        return jsonify("Invalid ID"), 400
    
    user = users.find_one({"_id": user_id})
    print(user)
    if user:
        output = {"name": user["name"], "email": user["email"]}
    else:
        output = "No results found"
    return jsonify(output)


@app.route("/users/<id>", methods=["PUT"])
def update_user(id):
    user = request.get_json()
    users.update_one({"_id": ObjectId(id)}, {"$set": user})
    return jsonify({"result": "User updated successfully"})


@app.route("/delete/<id>", methods=["DELETE"])
def delete_user(id):
    print("delete " + id)
    try:
        users.delete_one({"_id": ObjectId(id)})
    except:
        return jsonify({"result": "User not found"})
    return jsonify({"result": "User deleted successfully"})


app.run(debug=True)