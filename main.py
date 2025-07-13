from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import json
import os

app = FastAPI()

# Allow CORS from anywhere (frontend will call this)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # in production, specify your domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DB_FILE = 'db.json'

def load_db():
    if not os.path.exists(DB_FILE):
        with open(DB_FILE, 'w') as f:
            json.dump({'users': {}}, f)
    with open(DB_FILE, 'r') as f:
        return json.load(f)

def save_db(data):
    with open(DB_FILE, 'w') as f:
        json.dump(data, f, indent=2)

@app.post("/register")
async def register(request: Request):
    data = load_db()
    body = await request.json()
    username = body.get('username')
    password = body.get('password')
    if username in data['users']:
        return {"error": "Username already exists"}
    data['users'][username] = {
        "password": password,
        "coins": 100
    }
    save_db(data)
    return {"message": "Registered"}

@app.post("/login")
async def login(request: Request):
    data = load_db()
    body = await request.json()
    username = body.get('username')
    password = body.get('password')
    user = data['users'].get(username)
    if not user or user['password'] != password:
        return {"error": "Invalid credentials"}
    return {"message": "Login successful", "user": user}
