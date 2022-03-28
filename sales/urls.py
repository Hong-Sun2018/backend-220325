from django.urls import path
from . import views

urlpatterns = [
  path('test/', views.test),
  path('clear/', views.clear),
  path('read-from-file/', views.read_file),
  path('get-total-num-mysql/',views.get_total_num_mysql),
  path('get-min-max-date/', views.get_min_and_max_date),
  path('get-sum/', views.get_sum),
  path('list-sales/', views.get_sale_list),
]