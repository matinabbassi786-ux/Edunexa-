from django.contrib import admin
from django.urls import path,include
from tasks import test_task
from django.http import HttpResponse
from django.conf import settings
from django.urls import include, path

def test(request):
    test_task.delay("Some Name")
    return HttpResponse(f"Task ID: ")


urlpatterns = [
    path('', test, name='test'),
    path('admin/', admin.site.urls),
    path("api/",include('API.urls')),
]
