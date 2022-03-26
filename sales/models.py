from django.db import models

# Create your models here.
class Sale(models.Model): 
  product_id = models.CharField(max_length=10)
  store_id = models.CharField(max_length=10)
  date = models.CharField(max_length=10)
  sales = models.DecimalField(max_digits=15, decimal_places=1, null=True)
  revenue = models.DecimalField(max_digits=15, decimal_places=2, null=True)
  stock = models.DecimalField(max_digits=15, decimal_places=1, null=True)
  price = models.DecimalField(max_digits=15, decimal_places=2, null=True)

