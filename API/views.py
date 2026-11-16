from django.shortcuts import render,redirect
from rest_framework.decorators import api_view
from rest_framework.response import Response
from security.security  import user_authentication

@api_view(['GET', 'POST'])
def Index(request):
    
    if user_authentication(request) != False: return user_authentication(request)
    
    Data = {
        "messenge":"Wlecome to Edunexa "
    }
    return Response(Data)
  