from flask import Flask, request, jsonify
from flask_socketio import SocketIO, emit
import sqlite3

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

# DB setup
def init_db():
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS users (username TEXT PRIMARY KEY, password TEXT)")
    c.execute("CREATE TABLE IF NOT EXISTS games (id INTEGER PRIMARY KEY AUTOINCREMENT, data TEXT)")
    conn.commit()
    conn.close()
init_db()

@app.route("/login", methods=["POST"])
def login():
    data = request.json
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username=? AND password=?", (data["username"], data["password"]))
    user = c.fetchone()
    conn.close()
    return jsonify({"success": bool(user)})

@app.route("/register", methods=["POST"])
def register():
    data = request.json
    try:
        conn = sqlite3.connect("users.db")
        c = conn.cursor()
        c.execute("INSERT INTO users VALUES (?,?)", (data["username"], data["password"]))
        conn.commit()
        conn.close()
        return jsonify({"success": True})
    except:
        return jsonify({"success": False})

@app.route("/publish", methods=["POST"])
def publish():
    data = request.json
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("INSERT INTO games (data) VALUES (?)", (str(data),))
    conn.commit()
    conn.close()
    return jsonify({"success": True})

# Multiplayer demo
players = {}
@socketio.on("connect")
def connect():
    players[request.sid] = {"x":0,"y":0,"z":0}
    emit("update", players, broadcast=True)

@socketio.on("move")
def move(pos):
    players[request.sid] = pos
    emit("update", players, broadcast=True)

@socketio.on("disconnect")
def disconnect():
    players.pop(request.sid, None)
    emit("update", players, broadcast=True)

@app.route("/")
def index():
    return "Game Hub backend đang chạy!"

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5000)
