from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('product/<int:pk>/', views.product_detail, name='product_detail'),
    path('product/<int:pk>/add/', views.add_to_cart, name='add_to_cart'),
    path('product/<int:pk>/decrease/', views.decrease_item_cart, name='decrease_item_cart'),
    path('cart/', views.cart_detail, name='cart_detail'),
    path('clearcart/', views.cart_clear, name='remove_from_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('search/', views.ajax_search, name='ajax_search'),
    path('categories/', views.categories_list, name='categories_list'),

]