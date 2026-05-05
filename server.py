from flask import Flask
from flask_socketio import SocketIO, emit

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

players = {}

@socketio.on('connect')
def handle_connect():
    players[request.sid] = {"x":0, "y":0, "z":0}
    emit("update", players, broadcast=True)

@socketio.on('move')
def handle_move(pos):
    players[request.sid] = pos
    emit("update", players, broadcast=True)

@socketio.on('disconnect')
def handle_disconnect():
    players.pop(request.sid, None)
    emit("update", players, broadcast=True)

@app.route("/")
def index():
    return "Flask-SocketIO server đang chạy!"

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5000)
