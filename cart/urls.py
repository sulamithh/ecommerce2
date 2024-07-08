from django.urls import path
from .views import CartItemListCreateView, CartItemDetailUpdateDeleteView

urlpatterns = [
    path('cartitems/', CartItemListCreateView.as_view(), name='cartitem-list-create'),
    path('cartitems/<int:pk>/', CartItemDetailUpdateDeleteView.as_view(), name='cartitem-detail-update-delete'),
]
