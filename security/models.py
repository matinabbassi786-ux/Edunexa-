from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator

class userhistory(models.Model):
    user_names = models.ForeignKey(User,on_delete=models.CASCADE,related_name="UserNames",null=True,blank=True)
    User_Type = models.CharField(max_length=50)
    User_Code = models.TextField(null=True,blank=True)
    Ip = models.TextField(null=True,blank=True)
    user_agent = models.TextField(null=True,blank=True)
    language = models.CharField(null=True,blank=True)
    host = models.CharField(null=True,blank=True)
    method = models.CharField(max_length=50,null=True,blank=True)
    Path = models.TextField()
    path_Short = models.TextField()
    found = models.BooleanField(default=False)
    Date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return str(self.id)

class Wronging(models.Model):
    
    Wronging_link = models.ForeignKey(userhistory,on_delete=models.CASCADE)
    Wronging = models.SmallIntegerField(validators=[MinValueValidator(-10), MaxValueValidator(10)])
    Wronging_Type = models.CharField(max_length=255)
    Date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return str(self.id)