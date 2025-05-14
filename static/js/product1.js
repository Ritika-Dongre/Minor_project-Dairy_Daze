// PRODUCT FILTERING
document.addEventListener("DOMContentLoaded", function () {
    const filterButtons = document.querySelectorAll(".filter");
    const productCards = document.querySelectorAll(".product-card");

    filterButtons.forEach(button => {
        button.addEventListener("click", function () {
            const category = this.getAttribute("data-category");

            // Remove "active" class from all buttons and add to the clicked one
            filterButtons.forEach(btn => btn.classList.remove("active"));
            this.classList.add("active");

            // Show or hide products based on selection
            productCards.forEach(card => {
                if (category === "all") {
                    card.classList.remove("hidden");
                } else {
                    card.getAttribute("data-category") === category
                        ? card.classList.remove("hidden")
                        : card.classList.add("hidden");
                }
            });
        });
    });

    //  DROPDOWN TOGGLE
    const toggle = document.getElementById("dropdownToggle");
    const menu = document.getElementById("dropdownMenu");

    toggle.addEventListener("click", function (e) {
        e.stopPropagation(); // Prevent it from triggering document click
        menu.classList.toggle("show");
    });

    // Hide dropdown if clicked outside
    document.addEventListener("click", function (event) {
      if (!toggle.contains(event.target) && !menu.contains(event.target)) {
        menu.style.display = "none";
      }
    });
});