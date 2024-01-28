const ws = new WebSocket('ws://localhost:8080');

// Handle opening of WebSocket connection to Node.js
ws.onopen = function() {
    console.log('Connected to Node.js WebSocket server');
    ws.send('Hello from the website!');
};

// Handle messages received from Node.js WebSocket server
ws.addEventListener("message", (e) => {
    console.log(e.data)
});