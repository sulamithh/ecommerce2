from rest_framework import serializers
from .models import Product

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'seller', 'created_at', 'updated_at', 'stock', 'quantity']
        read_only_fields = ['seller']