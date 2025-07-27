// Function to handle the "Let's Go!" button
function nextPage() {
    // Redirect to your main app/dashboard page
    // You can change 'home.html' to the real page you are building.
    window.location.href = 'home.html';
}

// Optional: Smooth scroll for footer links (if you make them scrollable anchors later)
document.querySelectorAll('.footer-links a').forEach(link => {
    link.addEventListener('click', function (e) {
        if (this.hash !== '') {
            e.preventDefault();
            const target = document.querySelector(this.hash);
            target.scrollIntoView({ behavior: 'smooth' });
        }
    });
});
