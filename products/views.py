from django.forms.models import model_to_dict
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from products.models import Product
from django.utils import timezone
import csv

# Create your views here.

@api_view(["GET"])
def test(request, *args, **kwargs):
  return Response({"msg": "test success"})

# import CSV to database
@api_view(["GET"])
def read_products(request, *args, **kwargs): 

  # if database is not empty, skip import
  if Product.objects.count()>=1 :
    return Response({"msg": "products already exist in database."}, status=status.HTTP_304_NOT_MODIFIED)
  start_time = timezone.now()
  with open(".\csv_dataset\products.csv", "r") as csv_file:
    data = csv.reader(csv_file, delimiter=",")
    next(data) # skip CSV header
    products = []
    for row in data:
      product = Product(
        product_id = row[0],
        cluster_id = row[4],
        hierarchy1_id = row[5],
        hierarchy2_id = row[6],
        hierarchy3_id = row[7],
        hierarchy4_id = row[8],
        hierarchy5_id = row[9],
      )
      products.append(product)
      if len(products) > 100000:       # reading 100 000 line at a time to limmit memory usage
        Product.objects.bulk_create(products)
        products = []
    if len(products)>0 :   # if read finished and not reached 100 000 line, 
      Product.objects.bulk_create(products)
    total_time = timezone.now() - start_time
    res_data = {
      "total-time": str(total_time), 
      "msg": "read products from CSV file"
    }
    return Response(res_data)

# delete all products
@api_view(["GET"])
def clear(req, *data, **options):
  start_time = timezone.now()
  if Product.objects.count() > 0:
    Product.objects.all().delete()
  total_time = timezone.now() - start_time
  return Response({"msg": "cleared product database.", "total-time": total_time})

