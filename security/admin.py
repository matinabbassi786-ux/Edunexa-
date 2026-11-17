from django.contrib import admin
from .models import userhistory,Wronging




class userhistoryAdmin(admin.ModelAdmin):
    list_display = ("id",'User_Type','user_names','Path',"Date","method","found")
    list_display_links =("id","User_Type")


admin.site.register(userhistory,userhistoryAdmin)
admin.site.register(Wronging)