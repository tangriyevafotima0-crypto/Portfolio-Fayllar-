// Portfolio v1 - JavaScript
// Handles smooth scroll, fade-in animations, and mobile menu

// Mobile menu toggle
const mobileMenuBtn = document.getElementById("mobileMenuBtn");
const navLinks = document.getElementById("navLinks");

mobileMenuBtn.addEventListener("click", function () {
    navLinks.classList.toggle("active");
});

// Close mobile menu when a link is clicked
const navItems = document.querySelectorAll(".nav-links a");
navItems.forEach(function (item) {
    item.addEventListener("click", function () {
        navLinks.classList.remove("active");
    });
});

// Smooth scroll for navigation links
document.querySelectorAll('a[href^="#"]').forEach(function (anchor) {
    anchor.addEventListener("click", function (e) {
        e.preventDefault();
        const targetId = this.getAttribute("href");
        const targetElement = document.querySelector(targetId);

        if (targetElement) {
            targetElement.scrollIntoView({
                behavior: "smooth",
                block: "start"
            });
        }
    });
});

// Fade-in animation on scroll using Intersection Observer
function setupFadeAnimations() {
    const fadeElements = document.querySelectorAll(".fade-in");

    const observer = new IntersectionObserver(function (entries) {
        entries.forEach(function (entry) {
            if (entry.isIntersecting) {
                entry.target.classList.add("visible");
                observer.unobserve(entry.target);
            }
        });
    }, {
        threshold: 0.1,
        rootMargin: "0px 0px -50px 0px"
    });

    fadeElements.forEach(function (element) {
        observer.observe(element);
    });
}

// Run animations when page loads
setupFadeAnimations();
