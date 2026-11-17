from django.shortcuts import render,redirect
from .models import userhistory
from django.urls import resolve, Resolver404
from django.http import HttpResponse
from django.utils.translation import get_language_from_request

import requests
import random
import string


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def check_url_status(url_path):
    try:
        resolve(url_path)
        return True
    except Resolver404:
        return False


def generate_code():
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choices(characters, k=500))


class SecurityMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        user_agents = request.META.get("HTTP_USER_AGENT", "")
        print(request.user.groups.all())
        if request.user.groups.filter(name='Admin').exists():
            Usertp = "Admin"
            print("*"*50)
            print("The Admin")
            print("*"*50)
        elif request.user.groups.filter(name='Student').exists():
            print("*"*50)
            Usertp = "Student"
            print("The Student")
            print("*"*50)
        elif request.user.groups.filter(name='Teacher').exists():
            print("*"*50)
            print("The Teacher")
            Usertp = "Teacher"
            print("*"*50)
        else:
            print("*"*50)
            Usertp = "Visitors"
            print("The Visitors")
            print("*"*50)


        #  User if loging then
        if request.user.is_authenticated:
            userhistory.objects.create(
                user_names=request.user,
                Path=request.build_absolute_uri(),
                method=request.method,
                found=check_url_status(request.path),
                user_agent = user_agents,
                Ip = request.META.get("REMOTE_ADDR"),
                language = request.META.get("HTTP_ACCEPT_LANGUAGE"),
                host =  request.get_host(),
                path_Short=request.path,
                User_Type =Usertp,
            )

        
        response = self.get_response(request)

        user_agents = request.META.get("HTTP_USER_AGENT", "")

        #  If User is not login then make tem user 
        if not request.user.is_authenticated:
            
            if not request.COOKIES.get("tapmuser"):
                response.set_cookie(
                    key='tapmuser',
                    value=generate_code(),
                    max_age=30 * 24 * 60 * 60
                )
        
        tapmuser = request.COOKIES.get('tapmuser')
        
        if request.user.is_authenticated == False:
            userhistory.objects.create(
                User_Code = tapmuser,
                Path=request.build_absolute_uri(),
                method=request.method,
                found=check_url_status(request.path),
                user_agent = user_agents,
                Ip = request.META.get("REMOTE_ADDR"),
                language = request.META.get("HTTP_ACCEPT_LANGUAGE"),
                host =  request.get_host(),
                path_Short=request.path,
                User_Type =Usertp,
                )

        return response