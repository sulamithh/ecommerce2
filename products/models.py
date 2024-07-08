from django.db import models
from accounts.models import User

# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='products')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    stock = models.IntegerField(default=0)
    quantity = models.IntegerField(default=0)

    def __str__(self):
        return self.name

    @property
    def stock_status(self, quantity_purchased):
        self.quantity -= quantity_purchased
        self.save()

        if self.quantity == 0:
            return "Out of stock"
        elif self.quantity < 5:
            return "Not enough in stock"
        else:
            return "In stock"
