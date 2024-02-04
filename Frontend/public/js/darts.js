const ws = new WebSocket("ws://localhost:8080");
const dartBoard = document.getElementById("dartBoard");

// Handle opening of WebSocket connection to Node.js

ws.onopen = function () {
  console.log("Connected to Node.js WebSocket server");
  ws.send("Hello from the website!");
};

// Handle messages received from Node.js WebSocket server

ws.addEventListener("message", (e) => {
  try {
    const data = JSON.parse(e.data);

    if (data.type === "image") {
      const decodedData = atob(data.content);
      
      // Convert to ArrayBuffer
      const arrayBuffer = new Uint8Array(decodedData.length);
      for (let i = 0; i < decodedData.length; i++) {
        arrayBuffer[i] = decodedData.charCodeAt(i);
      }

      // Create Blob
      const blob = new Blob([arrayBuffer], { type: "image/png" });
      dartBoard.src = URL.createObjectURL(blob);
    }
  } catch (error) {
    console.log("ERROR parsing JSON", error);
  }
});
