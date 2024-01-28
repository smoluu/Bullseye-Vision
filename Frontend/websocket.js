const WebSocket = require("ws");

function handle_WebSocket() {

// Start Websocket server
const wss = new WebSocket.Server({ port: 8080 });
// Start connection to python Websocket server
const pythonWebSocket = new WebSocket("ws://localhost:8765");

  wss.on("connection", (wss, req) => {
    console.log("New connection from:", req.socket.remoteAddress);

    // Forward messages from the website to Python WebSocket server
    wss.onmessage = (e) => {
      console.log("MESSAGE_FROM_WEBSITE", e.data);
      pythonWebSocket.send("MESSAGE_FROM_WEBSITE", e.data);
    };
  });
  wss.on("close",(code,reason) => {
    console.log(code);
    console.log(reason);

  });


  pythonWebSocket.on("open", () => {
    console.log("Connected to Python WebSocket server");
  });

  // Handle messages received from Python WebSocket server
  pythonWebSocket.on("message", (e, wss) => {
  });

}

module.exports = { handle_WebSocket };
