from rest_framework.response import Response
from rest_framework import status
from sales.models import Sale
from rest_framework.decorators import api_view
from control.views import read_control, update_control
import csv
from django.utils import timezone
from user.views import verify_session


# Create your views here.
@api_view(["GET"])
def test(req, *args, **kwargs):
  return Response({"msg":"test success"})

# Read data from CSV
@api_view(["POST"])
def read_file(req):
    control = read_control()
    if Sale.objects.count() > 0:   # if data exists, return not modified
      return Response({"msg": "sales already exist in database."}, status=status.HTTP_304_NOT_MODIFIED)
    elif control.is_reading_sale :  # if program is reading file, return conflict
      return Response({"msg": "reading sales data"}, status=status.HTTP_409_CONFLICT)
    else:    # reading file
      print('Readddddddddddddddddddddddddddddddddddd')
      count = 0
      control.is_reading_sale = True
      update_control(control)
      time_start = timezone.now()
      with open('.\csv_dataset\sales.csv', "r") as csv_file:
        data = csv.reader(csv_file)
        next(data)    # skip header
        sales = []
        for row in data: 
          sale = Sale()
          sale.product_id = row[0]
          sale.store_id = row[1]
          sale.date = row[2]
          if row[3]:
            sale.sales=row[3]
          if row[4]:
            sale.revenue=row[4]
          if row[5]:
            sale.stock = row[5]
          if row[6]:
            sale.price = row[6]
          sales.append(sale)
          if len(sales) >= 10000:   # push 10000 sales to data base
            Sale.objects.bulk_create(sales)
            sales=[]
            count += 10000
            print(count)
        if sales: 
          count += len(sales) 
          print(count)
          Sale.objects.bulk_create(sales)
        control.is_reading_sale = False    # mark as not reading
        total_time = timezone.now() - time_start
        control.time_read_sale = str(total_time) # update 
        update_control(control)
        return Response({
          "total-time": control.time_read_sale, 
          "msg": "read sales from CSV file"
        })    

# clear data in sales
@api_view(["DELETE"])
def clear(req):
  Sale.objects.all().delete()
  return Response({
    "msg": "sales cleared."
  })

@api_view(["GET"])
def get_total_num_mysql(req):
  session = req.COOKIES.get('session_id')
  if verify_session(session) == False:
    return Response({}, status=status.HTTP_401_UNAUTHORIZED)

  count = Sale.objects.all().count()
  return Response({'count': count})

