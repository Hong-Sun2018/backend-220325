from rest_framework.response import Response
from rest_framework import status
from sales.models import Sale
from rest_framework.decorators import api_view
from control.views import read_control, update_control
import csv
from django.utils import timezone
from user.views import verify_session
from products.views import big_query

#################################### Big Query #############################

# Get min & max date in sales
@api_view(['GET'])
def get_min_and_max_date(req):
  session = req.COOKIES.get('session_id')
  if verify_session(session) == False:
    return Response({}, status=status.HTTP_401_UNAUTHORIZED)
  
  query_str ="""
    SELECT min(date), max(date) FROM `my-city-charge.dataset_20220327.sales`
  """
  result = big_query(query_str)
  return Response({
    'msg': 'query success',
    'result': result
  })

@api_view(['GET'])
def get_sum(req):

  session = req.COOKIES.get('session_id')
  if verify_session(session) == False:
    return Response({}, status=status.HTTP_401_UNAUTHORIZED)

  h1 = req.GET.get('h1', '')
  start_date = req.GET.get('start_date', '')
  end_date = req.GET.get('end_date', '')
  if len(h1) == 0 or len(start_date) == 0 or len(end_date) == 0:
    return Response({}, status=status.HTTP_400_BAD_REQUEST)
  # start_date = '2018-01-01'
  # end_date = '2019-01-02'
  query_str = f"""
    SELECT ROUND(sum(table_sales.sales),0), ROUND(SUM(table_sales.revenue), 2)
    FROM `my-city-charge.dataset_20220327.products` as  products
    INNER JOIN 
    `my-city-charge.dataset_20220327.sales` as table_sales
    ON products.product_id = table_sales.product_id
    WHERE products.hierarchy1_id = '{h1}' 
    AND table_sales.date >= DATE('{start_date}')
    AND table_sales.date <= DATE('{end_date}')
    AND table_sales.sales != 0
    AND table_sales.revenue != 0
  """

  result = big_query(query_str)
  return Response({'result': result})

@api_view(['GET'])
def get_sale_list(req):
  session = req.COOKIES.get('session_id')
  if verify_session(session) == False:
    return Response({}, status=status.HTTP_401_UNAUTHORIZED)

  city_id = req.GET.get('city', '')
  start_date = req.GET.get('start_date', '')
  end_date = req.GET.get('end_date', '')
  if len(city_id) == 0 or len(start_date) == 0 or len(end_date) == 0:
    return Response({}, status=status.HTTP_400_BAD_REQUEST)

  query_str = f"""
    SELECT store_table.city_id, product_table.hierarchy1_id, 
      EXTRACT(YEAR FROM sale_table.date), EXTRACT(MONTH FROM sale_table.date), 
      SUM(sale_table.sales)
    OVER()
    FROM `dataset_20220327.stores` as store_table
    INNER JOIN `dataset_20220327.sales` as sale_table
    ON store_table.store_id = sale_table.store_id
    INNER JOIN `dataset_20220327.products` as product_table
    ON sale_table.product_id = product_table.product_id
    WHERE store_table.city_id = '{city_id}'
    AND sale_table.date >= DATE('{start_date}')
    AND sale_table.date <= DATE('{end_date}')
    ORDER BY sale_table.sales
    LIMIT 100;
  """
  result = big_query(query_str)
  return Response({'result':result})

#################################### MySQL ###############################

# Create your views here.
@api_view(["GET"])
def test(req, *args, **kwargs):
  return Response({"msg":"test success"})

# Read data from CSV
@api_view(["POST"])
def read_file(req):
    session = req.COOKIES.get('session_id')
    if verify_session(session) == False:
      return Response({}, status=status.HTTP_401_UNAUTHORIZED)

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

  session = req.COOKIES.get('session_id')
  if verify_session(session) == False:
    return Response({}, status=status.HTTP_401_UNAUTHORIZED)

  Sale.objects.all().delete()
  return Response({
    "msg": "sales cleared."
  })

# get total number of data in table
@api_view(["GET"])
def get_total_num_mysql(req):
  session = req.COOKIES.get('session_id')
  if verify_session(session) == False:
    return Response({}, status=status.HTTP_401_UNAUTHORIZED)

  count = Sale.objects.all().count()
  return Response({'count': count})

