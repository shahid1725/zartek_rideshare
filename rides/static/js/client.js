// client.js
const socket = new WebSocket('ws://localhost:8000/ride/123/track/');

socket.onmessage = function(event) {
    const data = JSON.parse(event.data);
    console.log('Received current location:', data.current_location);
    // Update UI with the received current location
}
