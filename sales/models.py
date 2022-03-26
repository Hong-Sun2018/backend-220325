from django.db import models

# Create your models here.
class Sale(models.Model): 
  product_id = models.CharField(max_length=10)
  store_id = models.CharField(max_length=10)
  date = models.CharField(max_length=10)
  sales = models.DecimalField(max_digits=15, decimal_places=1)
  revenue = models.DecimalField(max_digits=15, decimal_places=2)
  stock = models.DecimalField(max_digits=15, decimal_places=1)
  price = models.DecimalField(max_digits=15, decimal_places=2)
  promo_type_1 = models.CharField(max_length = 10, null=True)
  promo_bin_1 = models.CharField(max_length = 10, null=True )
  promo_type_2 = models.CharField(max_length = 10, null=True)
  

