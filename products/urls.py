from django.urls import path
from .views import ProductListCreateView, ProductDetailUpdateDeleteView, FetchProductsFromAPI, ProductListView

urlpatterns = [
    path('', ProductListCreateView.as_view(), name='product-list-create'),
    path('<int:pk>/', ProductDetailUpdateDeleteView.as_view(), name='product-detail-update-delete'),
    path('fetch_products/', FetchProductsFromAPI.as_view(), name='fetch-products'),
    path('list/', ProductListView.as_view(), name='product-list'),
]
