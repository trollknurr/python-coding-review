from django.db import models


class Order(models.Model):
    address = models.CharField(max_length=255)
    
    created_at = models.DateTimeField()
    modified_at = models.DateTimeField()


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    product_id = models.CharField(max_length=255)
    quantity = models.IntegerField()
    price = models.FloatField()
    

class WarehouseItem(models.Model):
    product_id = models.CharField(max_length=255)
    quantity = models.IntegerField()
    price = models.FloatField()