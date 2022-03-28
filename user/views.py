from django.forms.models import model_to_dict
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from products.models import Product
from django.utils import timezone
from user.models import User
import hashlib
import json
import random
import string

# Create your views here.
def hello_world(request): 
  x = 1
  y = 2
  return Response('hellow_world')

@api_view(['POST'])
def signup(req):
  body = json.loads(req.body.decode('utf-8')) # get json string from bytes, then convert to dict
  u_name = body['username'].strip() # trim string
  pwd = body['password'].strip()

  # if username or password is empty return bad request
  if len(u_name) == 0 or len(pwd) == 0 :
    return Response({'msg': 'invalid username or passowrd input'}, status=status.HTTP_400_BAD_REQUEST)
  # hide password using md5
  pwd = hashlib.md5(bytes(pwd, 'utf-8')).hexdigest()
  # print(pwd)

  # if user exist return conflict 
  if User.objects.filter(username = u_name).count() > 0 :
    return Response({'msg': 'user existed.'}, status=status.HTTP_409_CONFLICT)
  
  User.objects.create(
    username = u_name,
    password = pwd,
  )
  return Response({'msg': 'user registed'})

@api_view(['POST'])
def signin(req):
  body = json.loads(req.body.decode('utf-8'))
  u_name = body['username'].strip()
  pwd = body['password'].strip()

  # if username or password is empty return bad request
  if len(u_name) == 0 or len(pwd) == 0 :
    return Response({'msg': 'invalid username or passowrd input'}, status=status.HTTP_400_BAD_REQUEST)
  # hide password using md5
  pwd = hashlib.md5(bytes(pwd, 'utf-8')).hexdigest()
  # print(pwd)

  # if can't find user return unauthorized
  users = User.objects.filter(username=u_name).filter(password = pwd).filter(is_admin = True).all()
  if len(users) != 1:
    return Response({'msg': 'login failed'}, status=status.HTTP_401_UNAUTHORIZED)

  # random str, length of 32
  random_str = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(32)) 
  # make the random str unique
  random_str = random_str + str(users[0].user_id)
  # update user session id
  users[0].session_id = random_str
  users[0].save()

  response = JsonResponse({
    'username': users[0].username, 
    'user_id': users[0].user_id, 
    'msg': 'login success.',
  })
  response.set_cookie(
    key = 'session_id',
    value = random_str,
    httponly = True,
    secure = True,
  )
  return response

@api_view(['GET'])
def session_signin(req):
  
  # if no session_id in cookie or session_id is empty, return unauthorized
  cookie_session = req.COOKIES.get('session_id')
  if cookie_session == None :
    return Response({}, status=status.HTTP_401_UNAUTHORIZED)
  if len(cookie_session) == 0:
    return Response({}, status=status.HTTP_401_UNAUTHORIZED)
  
  # get user from DB, if no user return unauthorized
  users = User.objects.filter(session_id=cookie_session).all()
  if len(users) != 1:
    return Response({}, status=status.HTTP_401_UNAUTHORIZED)
  
  res_data = {
    'user_id': users[0].user_id,
    'username': users[0].username,
  }
   
  return Response(res_data)
  
@api_view(['GET'])
def signout(req):
  response = JsonResponse({})
  response.set_cookie(
    key = 'session_id',
    value = '', 
    httponly = True,
    secure = True,
  )
  return response

def verify_session(session):

  # no session or invalid length, verify failed
  if session == None:
    return False
  elif len(session) < 33: 
    return False
  
  # if can not find user by session_id, verify failed
  users = User.objects.filter(session_id = session).all()
  if len(users) != 1:
    return False
  # if the only user found by session_id is not admin, verify failed  
  elif users[0].is_admin == False:
    return False
  else:
    return True