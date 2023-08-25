# Sleek Boutique Django E-Commerce Project

Welcome to the Sleek Boutique Django E-Commerce project! This is a web application built using Django framework to create an online store where users can browse, add products to their cart, and place orders.

## Functionalities

- Browse products: Users can view a list of products available in the store.
- Product details: Users can view detailed information about a specific product.
- Add to cart: Users can add products to their shopping cart.
- Cart: Users can view their cart, update quantities, and remove items.
- Checkout: Users can place orders by providing shipping information and payment method.
- Order confirmation: Users receive an email confirmation after placing an order.

## Endpoints (URLs/Views)

- Home Page: `/listings/`
    - Displays a paginated list of available products.
    - Function: `listing_page` in `views.py`

- Product Detail Page: `/product/<product_id>/`
    - Displays detailed information about a specific product.
    - Function: `product_detail` in `views.py`

- Add to Cart: `/add_to_cart/<product_id>/<size>/`
    - Adds a product to the user's cart.
    - Function: `add_to_cart` in `views.py`

- Cart Page: `/cart/`
    - Displays the items in the user's cart, along with total price.
    - Functions: `cart`, `update_quantity`, `clear_cart`, `delete_cart_item` in `views.py`

- Search: `/search/`
    - Displays search results for products based on user input.
    - Function: `search` in `views.py`

- Checkout: `/checkout/`
    - Allows users to provide shipping information, contact info, and payment method for placing an order.
    - Functions: `checkout` in `views.py`

- Order Confirmation: `/order_confirmation/`
    - Displays order details and confirms the successful placement of the order.
    - HTML Template: `order_confirmation.html` in `templates/ecommerce`

## Setting Up the Project

1. Clone the repository:
git clone https://gitlab.arbisoft.com/saleha.shahzad/edited-saleha-shahzad.git
cd django_projects

2. Create a virtual environment and activate it:
```python
python -m venv venv
source venv/bin/activate
```
3. Install the project dependencies:
python -m pip install Django

4. Set up the database and apply migrations:
python manage.py migrate

5. Parse JSON data and populate the database:
python manage.py parse_json /path/to/filename.json

6. Run the development server:
python manage.py runserver

7. Access the application in your browser at `http://127.0.0.1:8000/`