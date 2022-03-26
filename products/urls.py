from django.urls import path
from . import views

# URL Config
urlpatterns = [
  path("read/", views.read_products),
  path("test/", views.test),
  path("clear/", views.clear),
]