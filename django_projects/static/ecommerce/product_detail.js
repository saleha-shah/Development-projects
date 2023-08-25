document.addEventListener("DOMContentLoaded", function() {
    const addToCartLinks = document.querySelectorAll(".add-to-cart-link");
    const sizeOptions = document.querySelectorAll(".size-options");

    addToCartLinks.forEach((link, index) => {
        link.addEventListener("click", function(event) {
            event.preventDefault();
            const selectedSize = sizeOptions[index].value;
            if (selectedSize) {
                const originalHref = link.getAttribute("href");
                const updatedHref = originalHref.replace("default", selectedSize);
                window.location.href = updatedHref;
            }
        });
    });
});