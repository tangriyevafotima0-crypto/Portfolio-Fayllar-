// Dark mode toggle with localStorage persistence

const darkModeBtn = document.getElementById("darkModeBtn");

// Check if user has a saved preference
function loadThemePreference() {
    const savedTheme = localStorage.getItem("theme");
    if (savedTheme === "dark") {
        document.body.setAttribute("data-theme", "dark");
        darkModeBtn.textContent = "☀️";
    }
}

// Toggle between light and dark mode
function toggleDarkMode() {
    const currentTheme = document.body.getAttribute("data-theme");

    if (currentTheme === "dark") {
        document.body.removeAttribute("data-theme");
        localStorage.setItem("theme", "light");
        darkModeBtn.textContent = "🌙";
    } else {
        document.body.setAttribute("data-theme", "dark");
        localStorage.setItem("theme", "dark");
        darkModeBtn.textContent = "☀️";
    }
}

// Set up event listener
darkModeBtn.addEventListener("click", toggleDarkMode);

// Load theme when page loads
loadThemePreference();
