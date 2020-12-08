from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    value = models.DecimalField(decimal_places=2, max_digits=10)
