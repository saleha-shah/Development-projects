from django.urls import path

from ecommerce import views

app_name = 'ecommerce'

urlpatterns = [
    path('listings/', views.listing_page, name='listings'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail')

]
