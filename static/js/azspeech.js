const voices = [
{"countryCode":"ar","voice":"ar-SA-ZariyahNeural"},
{"countryCode":"en","voice":"en-US-AvaMultilingualNeural"},
{"countryCode":"fr","voice":"fr-FR-DeniseNeural"},
{"countryCode":"de","voice":"de-DE-KatjaNeural"},
{"countryCode": "he","voice":"he-IL-HilaNeural"},
{"countryCode":"it","voice":"it-IT-ElsaNeural"},
{"countryCode":"ja","voice":"ja-JP-NanamiNeural"},
{"countryCode":"ru","voice":"ru-RU-SvetlanaNeural"},
{"countryCode":"es","voice":"es-MX-DaliaNeural"},
{"countryCode":"uk","voice":"uk-UA-PolinaNeural"},
{"countryCode":"zh","voice":"zh-CN-XiaoxiaoNeural"},
{"countryCode":"zu","voice":"zu-ZA-ThandoNeural"},
{"countryCode":"hi","voice":"hi-IN-AnanyaNeural"}
]

function getVoice(countryCode){
    for (const item of voices) {
        if (item["countryCode"] === countryCode) {
            return item["voice"];
        }
    }
    return undefined;
}

function synthesizeSpeech(inputText,voice) {
//  const text = document.getElementById("text").value;
//  const language = document.getElementById("language").value;
  debugger;
  fetch("/synthesize", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      text: inputText,
      language: voice,
    }),
  })
    .then((response) => response.blob())
    .then((blob) => {
      const url = URL.createObjectURL(blob);
      const audio = document.getElementById("audio");
      audio.src = url;
//      audio.play();
    })
    .catch((error) => {
      console.error("Error:", error);
    });
}


document.querySelector('#speakOriginal').addEventListener('click', () => {
  let originalLanguageCode = document.querySelector('#originalLanguageCode').textContent;
  console.log(originalLanguageCode)
  let voice = getVoice(originalLanguageCode)
  console.log(voice)
  let originalText = document.querySelector('#originalText').textContent
  debugger;
   synthesizeSpeech(originalText,voice)
});
document.querySelector('#speakTranslated').addEventListener('click', () => {

  let targetLanguageCode = document.querySelector('#targetLanguageCode').textContent;
  let voice = getVoice(targetLanguageCode);
  let translatedText = document.querySelector('#translatedText').textContent;
//   debugger;
   synthesizeSpeech(translatedText,voice)
});
