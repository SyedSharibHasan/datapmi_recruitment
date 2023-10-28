from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from functools import wraps
from django.views.decorators.csrf import csrf_protect,csrf_exempt
from django.views.generic import ListView,CreateView,UpdateView,DetailView,DeleteView
from .models import Candidate
from django.urls import reverse_lazy



def welcome(request):
    return render(request,'login.html')



def main(request):
    if request.user.is_superuser:
        # Redirect superuser to admin.html
        return render(request,'admin.html')
    else:
        # Redirect normal user to user.html
        return render(request,'user.html')
    


def signup(request):
    if request.method == "POST":
        username = request.POST.get("username")
        fname = request.POST.get("fname")
        lname = request.POST.get("lname")
        email = request.POST.get("email")
        pass1 = request.POST.get("pass1")
        pass2 = request.POST.get("pass2")

        if pass1 != pass2:
            return HttpResponse("Your password and confirm password are not same!!")
        else:
            myuser = User.objects.create_user(username, email, pass1)
            myuser.first_name = fname
            myuser.last_name = lname
            myuser.save()
            messages.success(request, "Your account has been successfully created.")

            return redirect("login")
    return render(request, 'signup.html')


@csrf_exempt
def signin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        pass1 = request.POST.get('pass1')
        user = authenticate(request, username=username, password=pass1)

        if user is not None:
            if user.is_superuser:
                # Redirect superuser to admin.html
                login(request, user)
                return render(request, 'admin.html')
            else:
                # Redirect normal user to user.html
                login(request, user)
                return render(request, 'user.html')
        else:
            return HttpResponse("Username or password is incorrect!!!")
    return render(request, 'login.html')




######## supseruser function for only authentiacting superuser
def superuser_login_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_superuser:
            return view_func(request, *args, **kwargs)
        else:
            return HttpResponse("Access denied. You must be a superuser.")
    return _wrapped_view



@superuser_login_required
def admin(request):
    return render(request,'admin.html')


@login_required
def user(request):
    candidate = Candidate.objects.all()
    return render(request,'user.html',context={'candidate':candidate})



class Createcandidate(CreateView):
    model = Candidate
    success_url= reverse_lazy('user')
    template_name = 'add_candidate.html'
    fields ="__all__"








