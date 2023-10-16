

from django.shortcuts import render, redirect



def welcome(request):
    return render(request,'login.html')





def main(request):
    if request.user.is_superuser:
        # Redirect superuser to admin.html
        return render(request,'admin.html')
    else:
        # Redirect normal user to user.html
        return render(request,'user.html')
    








