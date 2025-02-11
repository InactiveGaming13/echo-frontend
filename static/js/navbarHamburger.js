const hamburger = document.querySelector(".navbarHamburger");
const navbar = document.querySelector(".navbar");
const navbarMenu = document.querySelector(".navbarMenu");

hamburger.addEventListener("click", () => {
    hamburger.classList.toggle("active");
    navbarMenu.classList.toggle("active");
    navbar.classList.toggle("active");
});