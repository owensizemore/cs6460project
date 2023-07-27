let chunks = [];
let mediaRecorder;
let isRecording = false;
let startTime;
let updateInterval;

let recordSubmitButton = document.getElementById('recordSubmitButton')
let audioUrl;

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
        startTime = Date.now();

        mediaRecorder.addEventListener('dataavailable', function(event) {
            chunks.push(event.data);
        });

        mediaRecorder.start();

        isRecording = true;
        updateButtonState();

        // Update the button text with the recording duration every second
        updateInterval = setInterval(updateRecordingDuration, 1000);

        console.log("Recording started!");

        function updateRecordingDuration() {
            if (isRecording) {
                const elapsedTime = new Date(Date.now() - startTime);
                const minutes = String(elapsedTime.getMinutes()).padStart(2, '0');
                const seconds = String(elapsedTime.getSeconds()).padStart(2, '0');
                const durationText = `Recording... ${minutes}:${seconds}`;
                document.getElementById('recordButtonText').textContent = durationText;
            } else {
                clearInterval(updateInterval);
            }
        }
    })
    .catch(function(error) {
        console.error("Error accessing audio stream: ", error)
    })
}

function stopRecording() {
    mediaRecorder.stop();

    mediaRecorder.addEventListener('stop', function() {
        const audioBlob = new Blob(chunks, { type: 'audio/webm' });
        audioUrl = URL.createObjectURL(audioBlob);

        console.log("audioURL is: " + audioUrl)

        // Update the button text with the duration of the finished recording
        const recordingDuration = new Date(Date.now() - startTime);
        const minutes = String(recordingDuration.getMinutes()).padStart(2, '0');
        const seconds = String(recordingDuration.getSeconds()).padStart(2, '0');
        const durationText = `${minutes}:${seconds} -- Click to Start Over`;
        document.getElementById('recordButtonText').textContent = durationText;

        document.getElementById('recordButton').classList.remove('is-danger');
        document.getElementById('recordButton').classList.add('is-success');

        chunks = [];
        isRecording = false;
        updateButtonState();

        console.log("Recording stopped!");
    })
}

function updateButtonState() {
    const recordButton = document.getElementById('recordButton');
    const recordIcon = document.getElementById('recordIcon');
    const recordSubmitButton = document.getElementById('recordSubmitButton');

    if (isRecording) {
        recordButton.classList.remove('is-info');
        recordButton.classList.add('is-danger');
        recordIcon.innerHTML = '<i class="fas fa-stop"></i>';
        recordSubmitButton.setAttribute('disabled', 'disabled');
        recordSubmitButton.classList.add('is-outlined');
    } else {
        recordButton.classList.remove('is-danger');
        recordButton.classList.add('is-success');
        recordIcon.innerHTML = '<i class="fas fa-check"></i>';
        recordSubmitButton.removeAttribute('disabled');
        recordSubmitButton.classList.remove('is-outlined');
    }
}

recordSubmitButton.addEventListener('click', downloadAudio);

function downloadAudio() {    
    const downloadLink = document.createElement('a');
    downloadLink.href = audioUrl;

    downloadLink.download = 'recorded_audio.ogg';

    document.body.appendChild(downloadLink);
    downloadLink.click();

    document.body.removeChild(downloadLink);
}