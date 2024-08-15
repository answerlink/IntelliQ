const startButton = document.getElementById('start');
const stopButton = document.getElementById('stop');
const transcriptDisplay = document.getElementById('transcript');

let mediaRecorder;
let websocket;

startButton.addEventListener('click', async () => {
    // Get user's audio input
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    
    // Create a WebSocket connection to the server
    websocket = new WebSocket('ws://localhost:43007');
    
    websocket.onopen = () => {
        console.log('WebSocket connection opened');
        startButton.disabled = true;
        stopButton.disabled = false;
    };
    
    websocket.onmessage = (event) => {
        // Display the transcribed text
        const transcript = event.data;
        transcriptDisplay.textContent += transcript + '\n';
    };
    
    websocket.onclose = () => {
        console.log('WebSocket connection closed');
        startButton.disabled = false;
        stopButton.disabled = true;
    };
    
    websocket.onerror = (error) => {
        console.error('WebSocket error:', error);
    };
    
    // Create a MediaRecorder to capture audio stream
    mediaRecorder = new MediaRecorder(stream, { mimeType: 'audio/webm' });
    
    mediaRecorder.ondataavailable = (event) => {
        if (event.data.size > 0 && websocket.readyState === WebSocket.OPEN) {
            websocket.send(event.data);
        }
    };
    
    mediaRecorder.start(1000); // Send audio data every second
});

stopButton.addEventListener('click', () => {
    mediaRecorder.stop();
    websocket.close();
    startButton.disabled = false;
    stopButton.disabled = true;
});
