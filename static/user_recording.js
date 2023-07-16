let chunks = [];
let mediaRecorder;
let isRecording = false;

function toggleRecording() {
    if (isRecording) {
        stopRecording();
    } else {
        startRecording();
    }
}

function startRecording() {
    navigator.mediaDevices.getUserMedia({ audio: true })
    .then(function(stream) {
        mediaRecorder = new MediaRecorder(stream);

        mediaRecorder.addEventListener('dataavailable', function(event) {
            chunks.push(event.data);
        });

        mediaRecorder.start();

        isRecording = true;
        updateButtonState();

        console.log("Recording started!");
    })
    .catch(function(error) {
        console.error("Error accessing audio stream: ", error)
    })
}

function stopRecording() {
    mediaRecorder.stop();

    mediaRecorder.addEventListener('stop', function() {
        const audioBlob = new Blob(chunks, { type: 'audio/webm' });
        const audioUrl = URL.createObjectURL(audioBlob);

        const audioDataInput = document.getElementById('audioData');
        audioDataInput.value = audioUrl;

        document.getElementById('userInputForm').style.display = 'block'; // This shows the form

        chunks = [];
        isRecording = false;
        updateButtonState();

        console.log("Recording stopped!");
    })
}

function updateButtonState() {
    const recordButton = document.getElementById('recordButton');
    const recordIcon = document.getElementById('recordIcon');

    if (isRecording) {
        recordButton.classList.remove('is-info');
        recordButton.classList.add('is-danger');
        recordIcon.innerHTML = '<i class="fas fa-stop"></i>';
    } else {
        recordButton.classList.remove('is-danger');
        recordButton.classList.add('is-primary');
        recordIcon.innerHTML = '<i class="fas fa-microphone"></i>';
    }
}