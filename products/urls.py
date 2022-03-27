from django.urls import path
from . import views

# URL Config
urlpatterns = [
  path("read-from-file/", views.read_products),
  path("test/", views.test),
  path("clear/", views.clear),
  path("get-total-num-mysql/",views.get_total_num_mysql),
]