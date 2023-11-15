// Get the additional status dropdown element
var additionalStatusDropdown = document.getElementById("additional-status");
// Get the offer container div
var offerContainer = document.getElementById("offer-container");

// Add change event listener to the additional status dropdown
additionalStatusDropdown.addEventListener("change", function () {
    // If "R2 Select" or similar options are selected, display the offer container; otherwise, hide it
    offerContainer.style.display = additionalStatusDropdown.value.includes("R") ? "block" : "none";
});




// Get the status dropdown element
var statusDropdown = document.getElementById('status');
var additionalOptionsDiv = document.getElementById('additional-options');
var rejectionReasonDiv = document.getElementById('reason-for-rejection');

// Add change event listener to the status dropdown
statusDropdown.addEventListener('change', function () {
    // Display additional options or rejection reason based on status
    additionalOptionsDiv.style.display = statusDropdown.value === 'Screen Select' ? 'block' : 'none';
    rejectionReasonDiv.style.display = statusDropdown.value === 'Screen Reject' ? 'block' : 'none';
});

// No need to re-declare additionalStatusDropdown, as it's already declared above

// Get the additional status dropdown element
var reasonForRejectionDiv = document.getElementById('reason-for-r1-r2-r3-r4-rejection');

// Add change event listener to the additional status dropdown
additionalStatusDropdown.addEventListener('change', function () {
    // Display reason for rejection based on additional status
    reasonForRejectionDiv.style.display = additionalStatusDropdown.value.includes('Reject') ? 'block' : 'none';
});
