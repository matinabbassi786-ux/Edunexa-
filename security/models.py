from django.db import models
from django.contrib.auth.models import User



class userhistory(models.Model):
    user_names = models.ForeignKey(User,on_delete=models.CASCADE,related_name="UserNames",null=True,blank=True)
    User_Code = models.TextField(null=True,blank=True)
    Path = models.TextField()
    method = models.CharField(max_length=50,null=True,blank=True)
    found = models.BooleanField(default=False)
    Date = models.DateField(auto_now_add=True)

    
