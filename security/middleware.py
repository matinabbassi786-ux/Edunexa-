from django.shortcuts import render,redirect
from .models import userhistory
from django.urls import resolve, Resolver404
import requests
import random
import string


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

        # 1. Handle user history for authenticated users
        if request.user.is_authenticated:
            userhistory.objects.create(
                user_names=request.user,
                Path=request.build_absolute_uri(),
                method=request.method,
                found=check_url_status(request.path)
            )

        # 2. Get the response ONCE
        response = self.get_response(request)

        # 3. Handle unauthenticated visitor cookies
        if not request.user.is_authenticated:
            if not request.COOKIES.get("tapmuser"):
                response.set_cookie(
                    key='tapmuser',
                    value=generate_code(),
                    max_age=30 * 24 * 60 * 60
                )
        
        tapmuser = request.COOKIES.get('tapmuser')
        
        if request.user.is_authenticated == False:
            userhistory.objects.create(User_Code = tapmuser,Path=request.build_absolute_uri(),method=request.method,found=check_url_status(request.path))

        return response