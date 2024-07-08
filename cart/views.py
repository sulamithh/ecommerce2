from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import CartItem, Order
from .serializers import CartItemSerializer, AddCartItemSerializer
from products.models import Product
from rest_framework import serializers

class CartItemListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return CartItem.objects.filter(order__user=self.request.user, order__is_active=True)

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return AddCartItemSerializer
        return CartItemSerializer

    def perform_create(self, serializer):
        order, created = Order.objects.get_or_create(user=self.request.user, is_active=True)
        try:
            serializer.save(order=order)
            return Response({"message": "Товар успешно добавлен в корзину."}, status=status.HTTP_201_CREATED)
        except serializers.ValidationError as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class CartItemDetailUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return CartItem.objects.filter(order__user=self.request.user, order__is_active=True)

    def perform_update(self, serializer):
        cart_item = self.get_object()
        new_quantity = serializer.validated_data.get('quantity')

        if new_quantity > cart_item.product.quantity:
            raise serializers.ValidationError(f"Недостаточно товара {cart_item.product.name} в наличии.")

        cart_item.product.quantity -= (new_quantity - cart_item.quantity)
        cart_item.product.save()
        serializer.save()
        return Response({"message": "Количество товара в корзине успешно обновлено."}, status=status.HTTP_200_OK)

    def perform_destroy(self, instance):
        instance.delete()
        return Response({"message": "Товар успешно удален из корзины."}, status=status.HTTP_204_NO_CONTENT)
