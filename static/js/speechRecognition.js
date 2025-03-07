document.addEventListener("DOMContentLoaded", () => {
  document.querySelector("#speakInput").addEventListener("click", (event) => {
    startRecognition(event);
  });
});

function startRecognition(event) {
  if (event) {
    // Prevent default form submission or other default behavior
    event.preventDefault();
  } else {
    console.log("Event object is null");
  }

  let languageCodeSelect = document.querySelector("#speechLanguageSelect");
  let languageCode =
    languageCodeSelect.options[languageCodeSelect.selectedIndex].value;
  let apiCall = "/start_recognition?language_code=" + languageCode;

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
