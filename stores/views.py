from rest_framework.response import Response
from rest_framework import status
from stores.models import Store
from rest_framework.decorators import api_view
from control.views import read_control, update_control
import csv
from django.utils import timezone

# Create your views here.

# Create your views here.
@api_view(["GET"])
def test(req, *args, **kwargs):
  return Response({"msg":"test success"})

# Read data from CSV
@api_view(["GET"])
def read_file(req, *args, **kwargs):
    control = read_control()
    if Store.objects.count() > 0:   # if data exists, return not modified
      return Response({"msg": "sales already exist in database."}, status=status.HTTP_304_NOT_MODIFIED)
    elif control.is_reading_store :  # if program is reading file, return conflict
      return Response({"msg": "reading sales data"}, status=status.HTTP_409_CONFLICT)
    else:    # reading file
      control.is_reading_store = True
      update_control(control)
      time_start = timezone.now()
      with open('.\csv_dataset\store.csv', "r") as csv_file:
        data = csv.reader(csv_file)
        next(data)    # skip header
        stores = []
        for row in data: 
          store = Store()
          store.store_id = row[0]
          store.storetype_id = row[1]
          store.store_size = row[2]
          store.city_id = row[3]
          stores.append(store)
          if len(stores) >100000:   # push 100000 sales to data base
            Store.objects.bulk_create(stores)
            stores=[]
        if stores: 
          Store.objects.bulk_create(stores)
        control.is_reading_store = False    # mark as not reading
        total_time = timezone.now() - time_start
        control.time_read_store = str(total_time)
        print(control.time_read_store)
        update_control(control)
        return Response({
          "total-time": control.time_read_store, 
          "msg": "read sales from CSV file"
        })
 

    
    

# clear data in sales
@api_view(["GET"])
def clear(req, *args, **kwargs):
  Store.objects.all().delete()
  return Response({
    "msg": "sales cleared."
  })
