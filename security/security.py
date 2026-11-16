from django.shortcuts import redirect


def user_authentication(request):
    try:
        if request.user.is_authenticated == False:
            return redirect("/login/")
        else: return False
    
    except:
        print(F"\033[31m ERROES \033[31m")
    