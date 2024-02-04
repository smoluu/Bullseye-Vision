const WebSocket = require("ws");

var wss;
var pythonWs;

var clients = [];

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
    pythonWs.send(
      JSON.stringify({
        message: "Nodejs is connected",
      })
    );
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

// handle client connection to websocket from website

wss.on("connection", (wss) => {
  clients.push(wss._socket.address().address);
  console.log(clients);

  // Send clients to python wss so it knows to send data or not

  pythonWs.send(
    JSON.stringify({
      clients: clients,
    })
  );

  // Forward messages from the client to Python WebSocket server

  wss.onmessage = (e) => {
    pythonWs.send(
      JSON.stringify({
        message: e.data,
      })
    );
  };

  // Handle messages received from Python WebSocket server

  pythonWs.on("message", (e) => {
    const data = JSON.parse(e)
    wss.send(JSON.stringify(data))
      

  });

  // Handle closing of connection

  wss.on("close", function () {
    const index = clients.indexOf(wss._socket.address().address);
    clients.splice(index, 1);
    pythonWs.send(
      JSON.stringify({
        clients: clients,
      })
    );
    console.log("CLIENT DISCONNECTED");
  });
});
