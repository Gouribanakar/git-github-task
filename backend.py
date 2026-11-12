import os
from flask import Flask, request, jsonify, render_template
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

client = MongoClient(os.getenv("MONGO_URI"))
db = client["todo_db"]
collection = db["todo_items"]

@app.route("/")
def home():
    return "Hello from Flask!"

@app.route("/todo")
def todo():
   return render_template("todo.html")

@app.route("/submittodoitem", methods=["POST"])
def submit_todo_item():
    # Accept both HTML form data and JSON
    item_name = request.form.get("itemName")
    item_description = request.form.get("itemDescription")

    if not item_name or not item_description:
        return jsonify({"error": "itemName and itemDescription are required"}), 400

    result = collection.insert_one({
        "itemName": item_name,
        "itemDescription": item_description
    })
    return jsonify({"message": "To-Do item saved", "id": str(result.inserted_id)}), 201

if __name__ == "__main__":
    app.run(debug=True)