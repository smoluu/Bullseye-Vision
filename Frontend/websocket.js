const WebSocket = require("ws");

var wss;
var pythonWs;

FgRed = "\x1b[31m";
FgGreen = "\x1b[32m";

// Start Websocket server
wss = new WebSocket.Server({ port: 8080 });

// Start connection to python Websocket server
connectToPytonWs = () => {
  var reconnectInterval = 5 * 1000;
  pythonWs = new WebSocket("ws://localhost:8765");

  pythonWs.on("open", function () {
    console.log(`${FgGreen}Socket connection succesfull: ${pythonWs.url}`, "\x1b[0m");
  });
  pythonWs.on("error", function () {
    console.log(`${FgRed}Socket connection error: ${pythonWs.url}`, "\x1b[0m");
  });
  pythonWs.on("close", function () {
    console.log(`Socket connection closed retrying in ${reconnectInterval / 1000} seconds`);
    setTimeout(connectToPytonWs, reconnectInterval);
  });
};
connectToPytonWs();

wss.on("connection", (wss, req) => {
  console.log("New connection from:", req.socket.remoteAddress);

  // Forward messages from the website to Python WebSocket server
  wss.onmessage = (e) => {
    console.log("MESSAGE_FROM_WEBSITE", e.data);
    pythonWs.send("MESSAGE_FROM_WEBSITE", e.data);
  };

  // Handle messages received from Python WebSocket server
  pythonWs.onmessage = function (e) {
    console.log("MESSAGE FROM PYTHONWS",e.data)
    wss.send(e.data)
  };
});

