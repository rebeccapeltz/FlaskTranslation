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
  synthesizeSpeech(originalText,originalLanguageCode, voice);
});
document.querySelector("#speakTranslated").addEventListener("click", () => {
  let translatedLanguageCode = document.querySelector(
    "#targetLanguageCode"
  ).textContent;
  let voice = getVoice(translatedLanguageCode);
  let translatedText = document.querySelector("#translatedText").textContent;
  synthesizeSpeech(translatedText,translatedLanguageCode, voice);
});

function getVoice(countryCode) {
  for (const item of voices) {
    if (item["countryCode"] === countryCode) {
      return item["voice"];
    }
  }
  return undefined;
}


function playAudioFromResponse(response) {
  response.blob().then(blob => {
      const audioUrl = URL.createObjectURL(blob);
      const audio = new Audio(audioUrl);
      audio.play();
  }).catch(error => {
      console.error("Error playing audio:", error);
  });
}


function synthesizeSpeech(input_text,language,voice) {
  input_text = input_text;
  language = language;
  voice =  voice;
  synthesize_get_url = `/synthesize?input_text=${input_text}&language=${language}&voice=${voice}`;
  console.log(synthesize_get_url)

  fetch(synthesize_get_url, {method: "GET"})
  .then(response => {
    if (!response.ok) {
        throw new Error('Network response was not ok');
    }
    playAudioFromResponse(response)
  })
  .catch(error => console.error('Error:', error));
}
