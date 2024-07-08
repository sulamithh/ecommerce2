from django.db import models
from django.contrib.auth import get_user_model
from products.models import Product
from orders.models import Order

User = get_user_model()

class CartItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='cart_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='cart_items')
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.product.name}"
