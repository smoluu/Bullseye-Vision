const ws = new WebSocket('ws://localhost:8080');

ws.onopen = function() {
    console.log('Connected to Node.js WebSocket server');
    ws.send('Hello from the website!');
};

// Handle messages received from Node.js WebSocket server
ws.onmessage = (e) => {
    console.log(`Received message from Node.js: ${e.data}`);
};


// Send messages to Node.js WebSocket server