const voices = [
  { countryCode: "ar", voice: "ar-SA-ZariyahNeural" },
  { countryCode: "en", voice: "en-US-AvaMultilingualNeural" },
  { countryCode: "fr", voice: "fr-FR-DeniseNeural" },
  { countryCode: "de", voice: "de-DE-KatjaNeural" },
  { countryCode: "he", voice: "he-IL-HilaNeural" },
  { countryCode: "it", voice: "it-IT-ElsaNeural" },
  { countryCode: "ja", voice: "ja-JP-NanamiNeural" },
  { countryCode: "ru", voice: "ru-RU-SvetlanaNeural" },
  { countryCode: "es", voice: "es-MX-DaliaNeural" },
  { countryCode: "uk", voice: "uk-UA-PolinaNeural" },
  { countryCode: "zh", voice: "zh-CN-XiaoxiaoNeural" },
  { countryCode: "zu", voice: "zu-ZA-ThandoNeural" },
  { countryCode: "hi", voice: "hi-IN-AnanyaNeural" },
];

document.querySelector("#speakOriginal").addEventListener("click", () => {
  let originalLanguageCode = document.querySelector(
    "#originalLanguageCode"
  ).textContent;
  let voice = getVoice(originalLanguageCode);
  let originalText = document.querySelector("#originalText").textContent;
  synthesizeSpeech(originalText, voice);
});
document.querySelector("#speakTranslated").addEventListener("click", () => {
  let translatedLanguageCode = document.querySelector(
    "#targetLanguageCode"
  ).textContent;
  let voice = getVoice(translatedLanguageCode);
  let translatedText = document.querySelector("#translatedText").textContent;
  synthesizeSpeech(translatedText, voice);
});

function getVoice(countryCode) {
  for (const item of voices) {
    if (item["countryCode"] === countryCode) {
      return item["voice"];
    }
  }
  return undefined;
}


const audioContext = new (window.AudioContext || window.webkitAudioContext)();

function base64ToArrayBuffer(base64) {
    const binaryString = atob(base64);
    const len = binaryString.length;
    const bytes = new Uint8Array(len);
    for (let i = 0; i < len; i++) {
        bytes[i] = binaryString.charCodeAt(i);
    }
    return bytes.buffer;
}

function playAudioFromBase64(base64Data) {
    const arrayBuffer = base64ToArrayBuffer(base64Data);
    audioContext.decodeAudioData(arrayBuffer, (buffer) => {
        const source = audioContext.createBufferSource();
        source.buffer = buffer;
        source.connect(audioContext.destination);
        source.start(0);
    }, (error) => {
        console.error('Error decoding audio data:', error);
    });
}


async function synthesizeSpeech(text, voice) {
  const urlWithParams = `/synthesize?text=${text}&voice=${voice}`;
  console.log(urlWithParams);
  try {
    const response = await fetch(urlWithParams);
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    const data = await response.json();
    playAudioFromBase64(data.audioData);
    // const audio = new Audio(
    //   `audioData:${data.contentType};base64,${data.audioData}`
    // );
    // playRawAudio(data.audioData,44.1,1)
    // audio.play();
  } catch (error) {
    console.error("Error fetching text-to-speech audio:", error);
    return null;
  }
}
// fetch('/speak?text=Hello, world!')
//   .then(response => response.json())
//   .then(data => {
//     const audio = new Audio(`data:${data.contentType};base64,${data.audioData}`);
//     audio.play();
//   });

// Fetch TTS from Backend
// const synthesizeSpeech = async (text, voice) => {
//   console.log(text, voice);
//   params = {
//     text: "Ciao",
//     voice: "it-IT-ElsaNeural",
//   };
//   const urlWithParams = `/synthesize?text=${text}&voice=${voice}`;
//   try {
//     const response = await fetch(urlWithParams);
//     if (!response.ok) {
//       throw new Error(`HTTP error! status: ${response.status}`);
//     }

//     // const audioBuffer = await response.arrayBuffer();
//     // if (audioBuffer.byteLength > 0) {
//     //   const audioBlob = new Blob([audioBuffer], { type: "audio/mpeg" });
//     //   const audioUrl = URL.createObjectURL(audioBlob);
//     //   const audio = new Audio(audioUrl);
//     //   audio.play();
//     //   return audioBlob;
//     // } else {
//     //   console.error("Empty audio response");
//     //   return null;
//     // }
//   } catch (error) {
//     console.error("Error fetching text-to-speech audio:", error);
//     return null;
//   }
// };
