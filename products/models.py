from django.db import models

# Create your models here.
class Product(models.Model):
  product_id = models.CharField(max_length=10, primary_key=True)
  cluster_id = models.CharField(max_length=10, null=True)
  hierarchy1_id = models.CharField(max_length=10)
  hierarchy2_id = models.CharField(max_length=12)
  hierarchy3_id = models.CharField(max_length=15)
  hierarchy4_id = models.CharField(max_length=18)
  hierarchy5_id = models.CharField(max_length=20)

  


