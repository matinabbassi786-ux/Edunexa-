from django.shortcuts import render,redirect
from .models import userhistory
from django.urls import resolve, Resolver404
import requests


def check_url_status(url_path):
    try:
        resolve(url_path)
        return True
    except Resolver404:
        return False

    


class SecurityMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        
        if request.user.is_authenticated:
            userhistorydb = userhistory.objects.create()
            userhistorydb.user_names = request.user
            userhistorydb.Path = request.build_absolute_uri()
            userhistorydb.method = request.method
            userhistorydb.found = check_url_status(request.path)
            userhistorydb.save()


        response = self.get_response(request)

        return response
