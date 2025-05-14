document.addEventListener("DOMContentLoaded", function () {
    const params = new URLSearchParams(window.location.search);
    const productId = params.get("id");

    const products = {
        "milk-1": {
            title: "Farm Fresh Homogenised Cow Milk",
            img: "milk.png",
            oldPrice: "₹38",
            newPrice: "₹37",
            size: "500ml",
            stockStatus: "in stock"
        },
        "milk-2": {
            title: "Organic Buffalo Milk",
            img: "buffalo-milk.png",
            oldPrice: "₹50",
            newPrice: "₹48",
            size: "1L",
            stockStatus: "in stock"
        }
        
    };

    if (productId && products[productId]) {
        const product = products[productId];

        document.getElementById("breadcrumb-title").textContent = product.title;
        document.getElementById("product-title").textContent = product.title;
        document.getElementById("product-img").src = product.img;
        document.getElementById("old-price").textContent = product.oldPrice;
        document.getElementById("new-price").textContent = product.newPrice;
        document.getElementById("product-size").textContent = product.size;
        document.getElementById("stock-status").textContent = product.stockStatus;
    } else {
        document.querySelector(".product-container").innerHTML = "<h2>Product Not Found!</h2>";
    }
});