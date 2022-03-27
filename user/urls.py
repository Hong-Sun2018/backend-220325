from django.urls import path
from . import views

# URL Config
urlpatterns = [
  path('hello/', views.hello_world),
  path('signup/', views.signup),
  path('signin/', views.signin),
  path('session-signin/', views.session_signin),
  path('signout/', views.signout)
]

