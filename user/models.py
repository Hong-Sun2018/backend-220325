from django.db import models

# Create your models here.
class User(models.Model):
  user_id = models.IntegerField(primary_key=True)
  username = models.CharField(max_length=30, unique=True)
  password = models.CharField(max_length=32)
  token = models.CharField(max_length = 50, null=True)
  time_login = models.BigIntegerField(null=True)
  time_wrong_pwd = models.BigIntegerField(null=True)
  num_wrong_pwd = models.IntegerField(null=True)
  
  