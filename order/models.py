from django.contrib.auth import get_user_model
from django.db import models

from main.models import Product


class Order(models.Model):
    user = models.ForeignKey(get_user_model(),
                             on_delete=models.RESTRICT,
                             related_name='orders')
    total_sum = models.DecimalField(max_digits=10, decimal_places=2)
    address = models.CharField(max_length=100)
    notes = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    products = models.ManyToManyField(Product, through='OrderItem')


class OrderItem(models.Model):
    order = models.ForeignKey(Order,
                              on_delete=models.RESTRICT,
                              related_name='items')
    product = models.ForeignKey(Product,
                                on_delete=models.RESTRICT)
    quantity = models.SmallIntegerField(default=1)

