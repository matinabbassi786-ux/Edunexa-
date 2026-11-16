from django.shortcuts import render,redirect
from rest_framework.views import APIView
from rest_framework.response import Response


class Index(APIView):
    def get(self, request, format=None):
        Data = {
            "Names":"Pass db"
        }
        return Response(Data)
    def post(self, request):
        usernames = request.data.get("usernames", [])
        return Response({"message": f"POST received from {usernames}"})

