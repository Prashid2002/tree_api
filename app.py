
from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
from werkzeug.security import check_password_hash

# Flask Setup
app = Flask(__name__)
CORS(app)

# MongoDB Atlas Connection
client = MongoClient("mongodb+srv://prashid:pranusim0@cluster0.ha6azez.mongodb.net/")
db = client["user_db"]

users_col = db["users"]
tree_col = db["tree_data"]

@app.route('/')
def hello():
    return "API is running."

@app.route('/api/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        username = data.get("username")
        password = data.get("password")

        if not username or not password:
            return jsonify({"error": "Username and password required"}), 400

        # Authenticate user
        user = users_col.find_one({"username": username})
        if not user:
            return jsonify({"error": "User not found"}), 404

        if not check_password_hash(user["password"], password):
            return jsonify({"error": "Invalid password"}), 401

        session_id = user.get("session_id")

        # Fetch tree data
        tree_doc = tree_col.find_one({"session_id": session_id}, {"_id": 0})
        tree_data = tree_doc.get("tree", []) if tree_doc else []

        # Return combined response
        return jsonify({
            "message": "Login successful",
            "session_id": session_id,
            "tree": tree_data
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
