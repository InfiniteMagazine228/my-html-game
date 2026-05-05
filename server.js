const express = require("express");
const http = require("http");
const { Server } = require("socket.io");

const app = express();
const server = http.createServer(app);
const io = new Server(server, { cors: { origin: "*" } });

let players = {};

io.on("connection", (socket) => {
  console.log("Người chơi kết nối:", socket.id);
  players[socket.id] = { x:0, y:0, z:0 };

  socket.on("move", (pos) => {
    players[socket.id] = pos;
    io.emit("update", players);
  });

  socket.on("disconnect", () => {
    delete players[socket.id];
    io.emit("update", players);
  });
});

// Dùng PORT của Render
const PORT = process.env.PORT || 3000;
server.listen(PORT, () => {
  console.log("Server chạy ở cổng " + PORT);
});
