from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import psycopg2

app = Flask(__name__)
CORS(app)

def get_db():
    return psycopg2.connect(
        host=os.getenv("DB_HOST", "database"),
        database=os.getenv("DB_NAME", "login_db"),
        user=os.getenv("DB_USER", "postgres"),
        password=os.getenv("DB_PASSWORD", "password123")
    )

@app.route("/login", methods=["POST"])
def login():
    data = request.json

    conn = get_db()
    cur = conn.cursor()

    cur.execute(
        "SELECT id FROM users WHERE username=%s AND password=%s",
        (data["username"], data["password"])
    )

    user = cur.fetchone()

    cur.close()
    conn.close()

    if user:
        return jsonify({"message": "Login successful!"})

    return jsonify({"message": "Invalid username or password"}), 401

@app.route("/health")
def health():
    return jsonify({"status": "Backend running"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
