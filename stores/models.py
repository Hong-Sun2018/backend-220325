from django.db import models

# Create your models here.
class Store(models.Model): 
  store_id = models.CharField(max_length=10)
  storetype_id = models.CharField(max_length=10)
  store_size = models.IntegerField()
  city_id = models.CharField(max_length=10)