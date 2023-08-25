function deleteCartItem(itemId) {
    fetch('/delete_cart_item/' + itemId + '/')
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                location.reload();
            }
        });
}
document.addEventListener("DOMContentLoaded", function() {
    const quantityButtons = document.querySelectorAll(".quantity-btn");
    const clearCartButton = document.querySelector(".clear-cart-btn");

    quantityButtons.forEach(button => {
        button.addEventListener("click", function(event) {
            event.preventDefault();
            const action = button.getAttribute("data-action");
            const itemId = button.getAttribute("data-item");
            updateQuantity(action, itemId);
        });
    });

    clearCartButton.addEventListener("click", function(event) {
        event.preventDefault();
        clearCart();
    });

    function updateQuantity(action, itemId) {
        fetch(`/update_quantity/${itemId}/${action}`)
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    window.location.reload();
                }
            })
            .catch(error => {
                console.error("Error updating quantity:", error);
            });
    }

    function clearCart() {
        fetch("/clear_cart")
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    window.location.reload();
                }
            })
            .catch(error => {
                console.error("Error clearing cart:", error);
            });
    }
});
