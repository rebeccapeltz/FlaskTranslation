const languageSelectElement = document.getElementById("speechLanguageSelect");
const speechOffButton = document.querySelector("#speechOff");
const speechOnButton = document.querySelector("#speechOn");
const inputText = document.querySelector("#input_text");
let language;
let mediaRecorder;
let localStream;
let audioChunks = [];


/**
 * Get file extension from mime type
 * @param {} mimeType 
 * @returns file extension or "unknown"
 */
function getFileExtension(mimeType) {
  const mimeExtensions = {
    "audio/webm": "webm",
    "audio/webm;codecs=pcm": "webm",
    "audio/webm;codecs=opus": "webm",
    "audio/ogg": "ogg",
    "audio/ogg;codecs=opus": "ogg",
    "audio/wav": "wav",
    "audio/x-wav": "wav",
    "audio/vnd.wave": "wav",
    "audio/mpeg": "mp3",
    "audio/mp3": "mp3",
    "audio/mp4": "mp4",
    "audio/aac": "aac",
    "audio/flac": "flac",
    "audio/x-m4a": "m4a",
    "audio/m4a": "m4a",
  };
  return mimeExtensions[mimeType] || "unknown";
}

/**
 * Determine the browser's supported mime type
 * @returns supported mime type
 */
function getSupportedMimeType() {
  const mimeTypes = [
    "audio/wav",
    "audio/webm;codecs=pcm",
    "audio/webm;codecs=opus",
    "audio/mp4",
  ];
  return mimeTypes.find((type) => MediaRecorder.isTypeSupported(type)) || "";
}


/**
 * Send blob of collected audio chunks to server
 * Assigns recognized text to the input text area
 * @param {} audioBlob 
 * @param {*} mimeType 
 * @param {*} language 
 */

// send blob collected in browser to server and record text response
// https://learn.microsoft.com/en-us/azure/ai-services/speech-service/rest-speech-to-text-short

async function sendRawAudioToServer(audioBlob, mimeType, language) {
  const formData = new FormData();
  const fileExtension = getFileExtension(mimeType);
  formData.append("audio", audioBlob, `audio.${fileExtension}`);
  formData.append("language", language);
  formData.append("format", "simple");
 
  const response = await fetch("/upload_audio", {
    method: "POST",
    body: formData
  });

  const result = await response.json();
  inputText.value = result.text;
  // reset language selection
  languageSelectElement.value = "none";
  console.log("Transcription from Flask:", result.text);
}

/**
 * Start recording audio from user
 */
async function startRecording() {
  // Request microphone access
  localStream = await navigator.mediaDevices.getUserMedia({ audio: true });
  const mimeType = getSupportedMimeType();
  console.log("Using audio format:", mimeType);

  // Instantiate media recorder with stream and mime type
  mediaRecorder = new MediaRecorder(localStream, { mimeType });

  // Capture audio chunks into array
  mediaRecorder.ondataavailable = (event) => {
    if (event.data.size > 0) {
      audioChunks.push(event.data);
    }
  };

  /***
   * Stop recording and send audio to server
   * Clear stream and audio chunks array
   */
  
  mediaRecorder.onstop = async () => {
    debugger;
   
    const blob = new Blob(audioChunks, { type: mimeType });
    if (localStream) {
      localStream.getTracks().forEach((track) => track.stop());
      localStream = null;
    }
    audioChunks = [];
    sendRawAudioToServer(blob, mimeType,language);
    
  };


  // Start recording
  mediaRecorder.start();
  console.log("Recording started...");
}

/***
 * Handler for UI call to stop recording
 */
function stopRecording() {
  if (mediaRecorder && mediaRecorder.state !== "inactive") {
    mediaRecorder.stop();
    console.log("Recording stopped.");
  }
}

/***
 * Manage state of language selection and speech buttons
 *  */ 

// default speech buttons nonclickable
speechOnButton.style.pointerEvents = "none";
speechOffButton.style.pointerEvents = "none";

// turn on speech off button when user clicks speech on button
speechOnButton.addEventListener("click", function (event) {
  // clear input text to allow for new text
  inputText.value = "";
  speechOffButton.classList.remove("btn-secondary");
  speechOffButton.classList.add("btn-danger");
  speechOffButton.style.pointerEvents = "auto";
  startRecording();
});

// turn off both buttons when user clicks speech off button
speechOffButton.addEventListener("click", function (event) {
  event.preventDefault();
  stopRecording();
  // disable speech buttons
  speechOnButton.classList.remove("btn-success");
  speechOnButton.classList.add("btn-secondary");
  speechOnButton.style.pointerEvents = "none";
  speechOffButton.classList.remove("btn-danger");
  speechOffButton.classList.add("btn-secondary");
  speechOffButton.style.pointerEvents = "none";
});

// update speech buttons based on language selection
languageSelectElement.addEventListener("change", function (event) {
  event.preventDefault();
  language = languageSelectElement.value;
  if (language === "none") {
    // buttons turn off if no language selected
    speechOnButton.style.pointerEvents = "none";
    speechOffButton.style.pointerEvents = "none";
    //set button colors to secondary (gray)
    speechOnButton.classList.remove("btn-success");
    speechOnButton.classList.add("btn-secondary");
    speechOffButton.classList.remove("btn-danger");
    speechOffButton.classList.add("btn-secondary");
  } else {
    //make speech on link clickable
    speechOnButton.style.pointerEvents = "auto";
    speechOnButton.classList.remove("btn-secondary");
    speechOnButton.classList.add("btn-success");
  }
});

