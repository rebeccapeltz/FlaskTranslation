if ("speechSynthesis" in window) {
    let voicesLoaded = false;
    let voiceRetryCount = 0;
    const MAX_VOICE_RETRIES = 5;
    let voiceList = [];
  
    function isFirefoxOrSafari() {
      return (
        /Firefox|Safari/i.test(navigator.userAgent) &&
        !/Chrome/.test(navigator.userAgent)
      );
    }
  
    function processVoices() {
      voiceList = window.speechSynthesis.getVoices();
      if (voicesLoaded.length > 0) voicesLoaded = true;
      console.log("Voices loaded:", voiceList);
      // Your voice processing logic here (filtering, selection, etc.)
    }
  
    function loadVoices() {
      processVoices();
  
      if (!voicesLoaded) {
        if (isFirefoxOrSafari()) {
          voiceList = window.speechSynthesis.getVoices();
          if (voiceList.length > 0) {
            processVoices();
          } else if (voiceRetryCount < MAX_VOICE_RETRIES) {
            voiceRetryCount++;
            setTimeout(loadVoices, 250); // Retry after 250ms
          } else {
            console.error(
              "Could not load voices after several attempts in Firefox or Safari."
            );
          }
        } else {
          // Chrome or Edge (listener allowed)
          window.speechSynthesis.addEventListener("voiceschanged", () => {
            processVoices();
            //   window.speechSynthesis.onvoiceschanged = () => {
          });
        }
      }
    }
  
    loadVoices();
  
    // Start loading voices when the page loads
  
    //Example of how to check if voices are loaded before attempting to speak.
    // function speakWhenReady(text, voiceName) {
    //   if (voicesLoaded) {
    //     speak(text, voiceName);
    //   } else {
    //     setTimeout(() => {
    //       speakWhenReady(text, voiceName);
    //     }, 100);
    //   }
    // }
  
    // console.log(voices);
    const speakOriginalBtn = document.querySelector("#speakOriginal");
    const speakTranslatedBtn = document.querySelector("#speakTranslated");
    let originalLanguage = document.querySelector(
      "#originalLanguageCode"
    ).textContent;
    let targetLanguage = document.querySelector(
      "#targetLanguageCode"
    ).textContent;
    let originalText = document.querySelector("#originalText").textContent;
    let translatedText = document.querySelector("#translatedText").textContent;
  
    // const synth = window.speechSynthesis;
  
    function selectVoice(voiceList, countryCode) {
      // get first voice that starts with country code
      console.log(voiceList);
      const filteredVoices = voiceList.filter((voice) =>
        voice.lang.startsWith(countryCode)
      );
      console.log(filteredVoices);
      const selectedVoice = filteredVoices.filter(item => item.name.startsWith('Rocko'));
      console.log(selectedVoice)
      return selectedVoice[0];
    }
    function speak(text, voice) {
      if (window.speechSynthesis.speaking) {
        console.error("speechSynthesis.speaking");
        return;
      }
  
      if (text !== "") {
        const utterThis = new SpeechSynthesisUtterance(text);
        utterThis.voice = voice;
        window.speechSynthesis.speak(utterThis);
      }
    }
    // window.speechSynthesis.addEventListener("voiceschanged", () => {
    //     var voices = window.speechSynthesis.getVoices();
  
    speakOriginalBtn.addEventListener("click", () => {
      // console.log(voices)
      //   voices = window.speechSynthesis.getVoices();
      debugger;
  
      let voice = selectVoice(voiceList, originalLanguage);
      speak(originalText, voice);
    });
  
    speakTranslatedBtn.addEventListener("click", () => {
      // console.log(voices)
      //   voices = window.speechSynthesis.getVoices();
      debugger
      let voice = selectVoice(voiceList, targetLanguage);
      debugger;
      speak(translatedText, voice);
    });
  }
  
  // const voicePreferences = {
  //     chrome: {
  //         'en-US': 'Google US English',
  //         'es-ES': 'Google Español',
  
  //     },
  //     safari: {
  //         'en-US': 'Samantha',
  //         'es-ES': 'Monica',
  //     },
  //     firefox: {
  //         'en-US': 'Microsoft David Desktop',
  //         'es-ES': 'Microsoft Helena Desktop',
  //     },
  //     edge: {
  //         'en-US': 'Microsoft David Desktop',
  //         'es-ES': 'Microsoft Helena Desktop',
  //     },
  // };