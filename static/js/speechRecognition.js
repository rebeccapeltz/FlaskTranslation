document.addEventListener("DOMContentLoaded", () => {
  // console.log('dom content loaded')
  document.querySelector("#speakInput").addEventListener("click", (event) => {
    if (event) event.preventDefault();
    startRecognition(event);
  });
});

function startRecognition(event) {
  // let languageCodeSelect = document.querySelector("#speechLanguageSelect");
  // let languageCode =
  //   languageCodeSelect.options[languageCodeSelect.selectedIndex].value;
  // let apiCall = "/start_recognition?language_code=" + languageCode;
  let apiCall = "/start_recognition";
  
  fetch(apiCall)
    .then((response) => response.json())
    .then((data) => {
      console.log(data);
      document.querySelector("#input_text").value = data.text;
    })
    .catch((error) => console.error("Error:", error));
}

// button to speak input initialized to disabled
document.querySelector("#speakInput").disabled = true;

const selectElement = document.getElementById("speechLanguageSelect");
selectElement.addEventListener("change", function () {
  const selectedValue = selectElement.value;
  if (selectedValue === "none") {
    //add disabled to button
    document.querySelector("#speakInput").disabled = true;
  } else {
    //remove disabled from button
    document.querySelector("#speakInput").disabled = false;
  }
});
