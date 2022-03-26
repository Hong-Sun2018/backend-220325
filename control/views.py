from rest_framework.response import Response
from rest_framework import status
from control.models import Control
from rest_framework.decorators import api_view

# Create your views here.

# Create
@api_view(['GET'])
def create(req, *args, **kwargs):
  if Control.objects.count() == 0:
    Control.objects.create(
      is_reading_prod = False,
      is_reading_sale = False,
      is_reading_store = False,
    )
    return Response({
      "msg": "create control success."
    })
  else: 
    return Response({
      "msg": "control existed."
    }, status=status.HTTP_304_NOT_MODIFIED)

# Read
# @api_view(['GET'])
def read_control():
  try: 
    control = Control.objects.get(id=1)
    return control
  except:
    return None

# update
def update_control(control):
  Control.objects.update(
    id = control.id,
    is_reading_prod = control.is_reading_prod,
    is_reading_sale = control.is_reading_sale,
    is_reading_store = control.is_reading_store,
    time_read_prod = control.time_read_prod,
    time_read_sale = control.time_read_sale,
    time_read_store = control.time_read_store,
  )