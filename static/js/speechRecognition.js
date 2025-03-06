document.addEventListener('DOMContentLoaded', (event) => {
    document.querySelector("#speakInput").addEventListener("click", startRecognition);
});

function startRecognition(event) {
    // Prevent default form submission or other default behavior
    event.preventDefault();

    let languageCodeSelect = document.querySelector("#speechLanguageSelect");
    let languageCode = languageCodeSelect.options[languageCodeSelect.selectedIndex].value;
    let apiCall = '/start_recognition?language_code=' + languageCode;

    fetch(apiCall)
        .then(response => response.json())
        .then(data => {
            console.log(data);
            document.querySelector("#input_text").value = data.text;
        })
        .catch(error => console.error('Error:', error));
}




//function startRecognitionOld(event) {
////    event.preventDefault();
//    // get selected language code
////    debugger
//    let languageCodeSelect = document.querySelector("#speechLanguageSelect");
//    let languageCode = languageCodeSelect.options[languageCodeSelect.selectedIndex].value;
//    let apiCall = '/start_recognition?language_code=' + languageCode
////    console.log(apiCall)
//
//    fetch(apiCall)
//        .then(response => response.json())
//        .then(data => {
////            debugger
//            console.log(data);
//            document.querySelector("#input_text").value = data.text;
//        })
//}

// button speak
//document.querySelector('#speakInput')
//button.disabled = true;

//const selectElement = document.getElementById('speechLanguageSelect');
//selectElement.addEventListener('change', function() {
//    const selectedValue = selectElement.value;
//    if (selectedValue === "none"){
//        //add disabled to button
//        document.querySelector('#speakInput').disabled = true;
//    } else {
//        //remove disabled from button
//        document.querySelector('#speakInput').disabled = false;
//    }
//
//});


