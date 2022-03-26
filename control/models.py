from django.db import models

# Create your models here.
class Control (models.Model): 
  is_reading_prod = models.BooleanField(default=False)
  time_read_prod = models.CharField(max_length=20, null=True)
  is_reading_sale = models.BooleanField(default=False)
  time_read_sale = models.CharField(max_length=20, null=True)
  is_reading_store = models.BooleanField(default=False)
  time_read_store = models.CharField(max_length=20, null=True)