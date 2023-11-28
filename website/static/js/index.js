

// Smooth scrolling to section when a link is clicked
document.addEventListener("DOMContentLoaded", function () {
    const links = document.querySelectorAll('a[href^="#"]');
    for (const link of links) {
        link.addEventListener("click", function (e) {
            e.preventDefault();
            const targetId = this.getAttribute("href").substring(1);
            const targetSection = document.getElementById(targetId);
            window.scrollTo({
                top: targetSection.offsetTop - 50, // Adjust for header height
                behavior: "smooth",
            });
        });
    }
});