// maternelle2.js

function loadContent(title) {
  const mainContent = document.getElementById("mainContent");
  mainContent.innerHTML = `
    <h2>${title}</h2>
    <p>This is where helpful content about <strong>${title}</strong> will go. You can customize this area with full articles, images, and more.</p>
  `;
}
