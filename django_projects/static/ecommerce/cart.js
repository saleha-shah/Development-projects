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
    const checkoutButton = document.querySelector(".checkout-btn");

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

    checkoutButton.addEventListener("click", function(event) {
        event.preventDefault();
        checkout();
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

    function checkout() {
        const selectedItems = Array.from(document.querySelectorAll("input[name='selected_items']:checked")).map(input => input.value);
        if (selectedItems.length === 0) {
            alert("Please select items to proceed with checkout.");
            return;
        }
        
        window.location.href = `/checkout?selected_items=${selectedItems.join(',')}`;
    }
});