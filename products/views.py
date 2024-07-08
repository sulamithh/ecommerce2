from django.shortcuts import render
from rest_framework import generics, filters
from .models import Product
from .serializers import ProductSerializer
from rest_framework.filters import SearchFilter, OrderingFilter
import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .permissions import IsSeller, IsBuyer
from django.contrib import messages

# Create your views here.
class ProductListCreateView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['name', 'description']
    ordering_fields = ['price', 'created_at']
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(seller=self.request.user)
        messages.success(self.request, "Товар успешно создан.")
        return Response({"message": "Товар успешно создан.", **serializer.data}, status=status.HTTP_201_CREATED)

    def get_permissions(self):
        if self.request.method == 'POST':
            self.permission_classes.append(IsSeller)
        return super().get_permissions()

class ProductDetailUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated, IsSeller]

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        messages.success(request, "Товар успешно обновлен.")
        return Response({"message": "Товар успешно обновлен.", **response.data})

    def destroy(self, request, *args, **kwargs):
        response = super().destroy(request, *args, **kwargs)
        messages.success(request, "Товар успешно удален.")
        return Response({"message": "Товар успешно удален."}, status=status.HTTP_204_NO_CONTENT)

    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            self.permission_classes.append(IsSeller)
        return super().get_permissions()

class FetchProductsFromAPI(APIView):
    def get(self, request, *args, **kwargs):
        response = requests.get('https://api.example.com/products')
        if response.status_code == 200:
            return Response(response.json(), status=status.HTTP_200_OK)
        else:
            return Response({"detail": "Не удалось получить товары."}, status=status.HTTP_400_BAD_REQUEST)

class ProductListView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description']
    ordering_fields = ['price', 'created_at']