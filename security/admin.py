from django.contrib import admin
from .models import userhistory




class userhistoryAdmin(admin.ModelAdmin):
    list_display = ("id",'user_names','Path',"Date","method","found")


admin.site.register(userhistory,userhistoryAdmin)