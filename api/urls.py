from django.urls import path
from .views import (
    ProductListAPIView, ProductDetailAPIView,
    ReviewCreateAPIView, ProfileAPIView
)

urlpatterns = [
    path('products/', ProductListAPIView.as_view(), name='api_products'),
    path('products/<int:pk>/', ProductDetailAPIView.as_view(), name='api_product_detail'),
    path('products/<int:pk>/reviews/', ReviewCreateAPIView.as_view(), name='api_product_review'),
    path('profile/', ProfileAPIView.as_view(), name='api_profile'),
]