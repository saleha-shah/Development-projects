from django.urls import path

from ecommerce import views

app_name = 'ecommerce'

urlpatterns = [
    path('listings/', views.listing_page, name='listings'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('cart/<int:product_id>/<str:size>/', views.add_to_cart, name='add_to_cart'),
    path('cart', views.cart, name='cart'),
    path('search', views.search, name='search'),
    path('delete_cart_item/<int:item_id>/', views.delete_cart_item, name='delete_cart_item'),
    path('update_quantity/<int:item_id>/<str:action>/', views.update_quantity),
    path('clear_cart/', views.clear_cart, name='clear_cart'),
    path('checkout/', views.checkout, name='checkout'),
]
