from django.urls import path
from . import views

urlpatterns = [
  path('test/', views.test),
  path('clear', views.clear),
  path('read', views.read_file),
  
]