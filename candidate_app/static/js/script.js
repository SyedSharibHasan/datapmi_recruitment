function toggleDarkMode() {
    var element = document.body;
    element.classList.toggle("dark-mode");

    // Toggle background image based on dark mode state
    if (element.classList.contains("dark-mode")) {
        element.style.backgroundImage = "none"; // Remove background image
    } else {
        element.style.backgroundImage = "url('/static/project_images/Profile.jpg')"; // Add background image
    }

    // Save the dark mode preference in local storage
    var darkModeEnabled = element.classList.contains("dark-mode");
    localStorage.setItem("darkMode", darkModeEnabled);

    // Toggle the dark mode icon
    var icon = document.getElementById("darkModeIcon");
    if (darkModeEnabled) {
        icon.classList.remove("bi-toggle2-off");
        icon.classList.add("bi-toggle2-on");
    } else {
        icon.classList.remove("bi-toggle2-on");
        icon.classList.add("bi-toggle2-off");
    }
}

// Apply dark mode on page load if the preference is saved
document.addEventListener("DOMContentLoaded", function () {
    var darkModeEnabled = localStorage.getItem("darkMode");
    if (darkModeEnabled === "true") {
        var element = document.body;
        element.classList.add("dark-mode");
        element.style.backgroundImage = "none"; // Remove background image when dark mode is enabled

        // Change the icon to the moon if dark mode is enabled
        var icon = document.getElementById("darkModeIcon");
        icon.classList.remove("bi-toggle2-off");
        icon.classList.add("bi-toggle2-on");
    }
});