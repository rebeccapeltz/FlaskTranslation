document.addEventListener("DOMContentLoaded", (event) => {

  const dropdownItems = document.querySelectorAll(".dropdown-item");

  // Loop through and add a click event listener to each item
  dropdownItems.forEach((item) => {
    item.addEventListener("click", function (event) {
      const selectedValue = event.target.textContent; // Get the text content of the clicked item
      if (selectedValue !== "none") {
        document.querySelector("#input_text").value = selectedValue;
      }
      console.log("Selected item:", selectedValue); // Log or process the selected value
    });
  });

});
