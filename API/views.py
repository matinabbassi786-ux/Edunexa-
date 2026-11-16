from django.shortcuts import render,redirect
from rest_framework.decorators import api_view
from rest_framework.response import Response
from security.security  import user_authentication
from django.contrib.auth import authenticate, login



@api_view(['GET', 'POST'])
def Index(request):
    Data = {
            "messenge":"Wlecome to Edunexa "
        }
      
    if user_authentication(request) != False: return user_authentication(request)

    if request.method == 'POST':
        usernames = request.data.get('usernames', None)
        password = request.data.get('password', None)
        Data.update({"usernames":usernames})
      
        if usernames == None or password == None: return Response({
            "usernames":"Enter you User Names",
            "password":"Enter you User password",
        })

        if isinstance(usernames, str) == False:return Response({"messenge":"User names is not string"})    
        if isinstance(password, str) == False:return Response({"messenge":"password is not string"})    
        if len(usernames) >= 150:return Response({"messenge":"You User names is laerger"})
        if len(password) >= 128:return Response({"messenge":"You password is laerger"})
        user = authenticate(request, username=usernames, password=password)
        if user is not None:
            login(request, user)
            return Response({"Done":"Pass"})

    return Response(Data)
  