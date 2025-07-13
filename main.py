from flask import Flask, request, jsonify, session
from flask_cors import CORS
import json
import os

app = Flask(__name__)
app.secret_key = "supersecretkey"
CORS(app)

DB_FILE = 'db.json'

def load_db():
    if not os.path.exists(DB_FILE):
        with open(DB_FILE, 'w') as f:
            json.dump({'users': {}, 'leaderboard': []}, f)
    with open(DB_FILE, 'r') as f:
        return json.load(f)

def save_db(data):
    with open(DB_FILE, 'w') as f:
        json.dump(data, f, indent=2)

@app.route('/')
def home():
    return jsonify({"message": "DrawQards Backend Working ✅"})

@app.route('/register', methods=['POST'])
def register():
    data = load_db()
    username = request.json.get('username')
    password = request.json.get('password')
    if not username or not password:
        return jsonify({'error': 'Missing username or password'}), 400
    if username in data['users']:
        return jsonify({'error': 'Username taken'}), 400
    data['users'][username] = {
        'password': password,
        'coins': 100,
        'deck': {},
        'xp': 0,
        'level': 1
    }
    save_db(data)
    return jsonify({'message': 'Registered successfully'})

@app.route('/login', methods=['POST'])
def login():
    data = load_db()
    username = request.json.get('username')
    password = request.json.get('password')
    user = data['users'].get(username)
    if not user or user['password'] != password:
        return jsonify({'error': 'Invalid credentials'}), 401
    session['username'] = username
    return jsonify({'message': 'Login successful', 'user': user})

@app.route('/deck', methods=['GET'])
def get_deck():
    username = session.get('username')
    if not username:
        return jsonify({'error': 'Not logged in'}), 401
    data = load_db()
    user = data['users'].get(username)
    return jsonify({'deck': user.get('deck', {})})

# Add your draw, sell, vault, etc. routes here too

if __name__ == '__main__':
    app.run()