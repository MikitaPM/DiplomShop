from django.urls import path
from . import views

urlpatterns = [
    path('cart_detail/', views.cart_detail, name='cart_detail'),
    path('cart_add/<product_id>/', views.cart_add, name='add'),
    path('cart_remove<product_id>/', views.cart_remove, name='remove'),

]