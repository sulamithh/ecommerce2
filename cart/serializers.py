from rest_framework import serializers
from .models import Order, CartItem
from products.models import Product

class CartItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    product_price = serializers.DecimalField(source='product.price', max_digits=10, decimal_places=2, read_only=True)
    product_seller = serializers.CharField(source='product.seller.username', read_only=True)

    class Meta:
        model = CartItem
        fields = ['id', 'order', 'product', 'product_name', 'product_price', 'product_seller', 'quantity']

class AddCartItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(write_only=True)

    class Meta:
        model = CartItem
        fields = ['product_name', 'quantity']

    def validate(self, data):
        product_name = data.get('product_name')
        quantity = data.get('quantity')

        try:
            product = Product.objects.get(name=product_name)
        except Product.DoesNotExist:
            raise serializers.ValidationError(f"Товар с названием {product_name} не существует")

        if quantity > product.quantity:
            raise serializers.ValidationError(f"Недостаточно товара {product_name} в наличии")

        data['product'] = product
        return data

    def create(self, validated_data):
        order = validated_data.get('order')
        product = validated_data.get('product')
        quantity = validated_data.get('quantity')

        cart_item, created = CartItem.objects.get_or_create(order=order, product=product)
        if created:
            cart_item.quantity = quantity
        else:
            if cart_item.quantity + quantity > product.quantity:
                raise serializers.ValidationError(f"Недостаточно товара {product.name} в наличии")
            cart_item.quantity += quantity
        cart_item.save()

        product.quantity -= quantity
        product.save()

        return cart_item

