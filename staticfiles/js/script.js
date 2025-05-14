document.addEventListener("DOMContentLoaded", function () {
    const menuToggle = document.querySelector(".menu-toggle");
    const navLinks = document.querySelector(".nav-links");
    const products = document.querySelectorAll(".product");

    // Mobile Menu Toggle
    menuToggle.addEventListener("click", function () {
        navLinks.style.display = navLinks.style.display === "flex" ? "none" : "flex";
    });

    // Scroll Effect for Floating Product Images
    let lastScrollTop = 0;
    window.addEventListener("scroll", function () {
        let scrollTop = window.pageYOffset || document.documentElement.scrollTop;
        
        if (scrollTop < lastScrollTop) {
            // Scrolling Up - Add Floating Effect
            products.forEach(product => product.classList.add("floating"));
        } else {
            // Scrolling Down - Remove Floating Effect
            products.forEach(product => product.classList.remove("floating"));
        }

        lastScrollTop = scrollTop;
    });
});

document.addEventListener("DOMContentLoaded", function () {
    const categoryButtons = document.querySelectorAll(".category-btn");
    const productCards = document.querySelectorAll(".product-card");

    categoryButtons.forEach(button => {
        button.addEventListener("click", function () {
            // Remove active class from all buttons
            categoryButtons.forEach(btn => btn.classList.remove("active"));
            this.classList.add("active");

            const category = this.getAttribute("data-category");

            // Show/hide products based on category
            productCards.forEach(card => {
                if (category === "all" || card.getAttribute("data-category") === category) {
                    card.style.display = "block";
                } else {
                    card.style.display = "none";
                }
            });
        });
    });
});

function filterProducts(category) {
    let products = document.querySelectorAll('.product-card');
    let buttons = document.querySelectorAll('.filter-btn');

    buttons.forEach(btn => btn.classList.remove('active')); 
    event.target.classList.add('active'); 

    products.forEach(product => {
        if (category === 'all' || product.classList.contains(category)) {
            product.style.display = 'block';
        } else {
            product.style.display = 'none';
        }
    });
}
