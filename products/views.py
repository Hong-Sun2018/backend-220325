from django.forms.models import model_to_dict
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from products.models import Product
from django.utils import timezone
import csv
# import os
# from google.cloud.bigquery import Client
from google.cloud import bigquery
from google.oauth2 import service_account
from user.views import verify_session
import pandas

# Create your views here.

######################################### Big Query ################################
def big_query(query_str):
  key_path = 'c:\\auth\\auth.json'
  credentials = service_account.Credentials.from_service_account_file(
    key_path, scopes=["https://www.googleapis.com/auth/cloud-platform"],
  )
  client = bigquery.Client(credentials=credentials, project=credentials.project_id,)

  dataframe = (
    client.query(query_str)
      .result()
      .to_dataframe()
  )
  list = dataframe.values.tolist()
  return list

# test
@api_view(["GET"])
def test(request, *args, **kwargs):
  query_string = """
    SELECT * FROM `my-city-charge.dataset_20220327.products` LIMIT 100
  """

  dataframe = big_query(query_string)

  print(dataframe)
  return Response({"msg": "test success", 'result': dataframe})

# get all hierarchy1
@api_view(['GET'])
def get_all_hierarchy1(req):
  
  session = req.COOKIES.get('session_id')
  if verify_session(session) == False:
    return Response({}, status=status.HTTP_401_UNAUTHORIZED)
  
  query_str = """
    SELECT DISTINCT  hierarchy1_id FROM `my-city-charge.dataset_20220327.products`
  """
  list = big_query(query_str)
  return Response({"msg": "query success", 'result': list})


########################################## MySQL ###########################################

# import CSV to database
@api_view(["POST"])
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
@api_view(["DELETE"])
def clear(req):
  start_time = timezone.now()
  if Product.objects.count() > 0:
    Product.objects.all().delete()
  total_time = timezone.now() - start_time
  return Response({"msg": "cleared product database.", "total-time": total_time})

@api_view(["GET"])
def get_total_num_mysql(req):
  session = req.COOKIES.get('session_id')
  if verify_session(session) == False:
    return Response({}, status=status.HTTP_401_UNAUTHORIZED)

  count = Product.objects.all().count()
  return Response({'count': count})

  
