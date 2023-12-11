// Get the additional status dropdown element
var additionalStatusDropdown = document.getElementById("additional-status");
// Get the offer container div
var offerContainer = document.getElementById("offer-container");

// Add change event listener to the additional status dropdown
additionalStatusDropdown.addEventListener("change", function () {
    // If "R2 Select" or similar options are selected, display the offer container; otherwise, hide it
    offerContainer.style.display = additionalStatusDropdown.value.includes("R") ? "block" : "none";
});





document.addEventListener('DOMContentLoaded', function () {
    var statusDropdown = document.getElementById('status');
    var additionalOptionsDiv = document.getElementById('additional-options');
    var additionalStatusDropdown = document.getElementById('additional-status');
    
    // Function to update display based on status
    function updateDisplay() {
      additionalOptionsDiv.style.display = statusDropdown.value === 'Screen Select' ? 'block' : 'none';
    }
  
    // Add change event listener to the status dropdown
    statusDropdown.addEventListener('change', function () {
      updateDisplay();
      
      // If 'Screen Select' is chosen, reset the additional status dropdown
      if (statusDropdown.value !== 'Screen Select') {
        additionalStatusDropdown.value = '';
      }
    });
  
    // Trigger the 'change' event when the page loads
    updateDisplay();
  });




  
// Get the additional status dropdown element
var reasonForRejectionDiv = document.getElementById('reason-for-r1-r2-r3-r4-rejection');

// Add change event listener to the additional status dropdown
additionalStatusDropdown.addEventListener('change', function () {
    // Display reason for rejection based on additional status
    reasonForRejectionDiv.style.display = additionalStatusDropdown.value.includes('Reject') ? 'block' : 'none';
});




          





