from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from functools import wraps
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView,CreateView,UpdateView,DetailView,DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import CustomUser
from .utils import generate_otp, send_otp_email
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .utils import send_recovery_link
from django.shortcuts import get_object_or_404
from finance_app.models import Employee
from candidate_app.models import Candidate


############  !!!!!!!!!!!!!!!!!     Account related , Admin ,  Common pages functionalities  are executed here .


######## registration
def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        pass1 = request.POST.get('pass1')
        pass2 = request.POST.get('pass2')

        username_exists = CustomUser.objects.filter(username=username).first()
        email_exists = CustomUser.objects.filter(email=email).first()
        
        if username_exists:
            return HttpResponse('Username already exists')
        
        if email:
            if not email.endswith('@datapmi.com'):
                return HttpResponse('Email format is not valid')

        if email_exists:
            return HttpResponse('Email already exists')

        if pass1 != pass2:
            return HttpResponse('Passwords are not matched')
        
        contact = request.POST.get('contact')
        role = request.POST.get('role')

        otp = generate_otp()
        send_otp_email(email, otp)

        request.session['username'] = username
        request.session['first_name'] = first_name
        request.session['last_name'] = last_name
        request.session['email'] = email
        request.session['password'] = pass1
        request.session['contact'] = contact
        request.session['role'] = role
        request.session['otp'] = otp

        return redirect('verify_otp')
    return render(request, 'signup.html')




####### after register otp verification process
def verify_otp(request):
    if request.method == 'POST':
        otp = request.POST.get('otp')
        email = request.session.get('email')
        stored_otp = request.session.get('otp')

        if otp == stored_otp:
            username = request.session.get('username')
            first_name = request.session.get('first_name')
            last_name = request.session.get('last_name')
            email = request.session.get('email')
            contact = request.session.get('contact')
            role = request.session.get('role')
            password = request.session.get('password')
            user = CustomUser.objects.create_user(
                username=username,
                first_name=first_name,
                last_name=last_name,
                email=email,
                contact=contact,
                role=role,
                password=password
            )
            user.save()
            login(request, user)
   
            if role == 'Recruiter':
                return redirect('user')  # Redirect to the 'user' page
            elif role == 'Finance':
                return redirect('finance_dashboard')  # Redirect to the 'finance_dashboard' page
            else:
                # Handle other roles or scenarios
                return HttpResponse("Your Selected Role does not satisfying our application. Contact Datapmi Team")
        else:
            messages.error(request, 'Invalid OTP Register Again !')    
            return redirect('signup')
    else:
        email = request.session.get('email')
        if not email:
            return redirect('signup')

    return render(request, 'otp_verification.html', {'email': email})





########## login + password recovery 
@csrf_exempt
def signin(request,action):
    if action == 'login':
        if request.method == 'POST':
            username = request.POST.get('username')
            pass1 = request.POST.get('pass1')
            user = authenticate(request, username=username, password=pass1)

            if user is not None:
                login(request, user)
                if user.is_superuser:
                    return redirect('admin') 
                
                elif user.role == 'Finance':
                    return redirect('finance_dashboard') 
                
                else:
                    return redirect('user')  
            else:
                return HttpResponse("Username or password is incorrect!!!")
    
    if action == 'recovery':  
        if request.method == 'POST':
            email = request.POST.get('email')
            user = CustomUser.objects.filter(email=email).first()

            if user:
                # Generate a unique token
                token = Signer().sign(user.id)

                user.password_reset_token = token
                user.password_reset_token_expiration = timezone.now() + datetime.timedelta(minutes=10)
                user.save()

                # Create the reset link with the token      ######## local host should be change after hosting for redirecting
                reset_link = f"http://122.165.80.8:8080/reset_password/{token}/"

                # Send recovery link
                send_recovery_link(email, reset_link)
                messages.success(request, 'Recovery link sent successfully. Check your email.')
                return redirect ('login_default')

            else:
                return HttpResponse("<script>alert('Email not found.'); window.location.href = '/login_default/';</script>")
    return render(request, 'login.html')




########### reset password and expiration process
import datetime
from django.utils import timezone
from django.core.signing import Signer
from django.core.signing import BadSignature

def reset_password(request, token):
    try:
        user_id = Signer().unsign(token)
        user = CustomUser.objects.get(id=user_id)

        # Check if the token is still valid (not expired)
        if user.password_reset_token_expiration and user.password_reset_token_expiration < timezone.localtime(timezone.now()):
            return render(request, 'reset_password_invalid.html')

    except (BadSignature, CustomUser.DoesNotExist):
        return render(request, 'reset_password_invalid.html')

    # If the token is valid and not expired, proceed with password reset logic
    if request.method == 'POST':
        # Reset password logic here
        password = request.POST.get('password')
        user.set_password(password)
        user.save()

        # Clear the token and expiration time after password reset
        user.password_reset_token = None
        user.password_reset_token_expiration = timezone.now() - datetime.timedelta(days=1)
        user.save()                 

        # Redirect to the login page after a successful password reset
        return redirect('login_default')  # Replace 'login_default' with the actual URL name for your login page

    # Pass the token to the template context
    context = {'token': token}
    return render(request, 'reset_password.html', context)





##############  logout
def signout(request):
    logout(request)
    return redirect('login_default')




######## supseruser function for only authentiacting superuser
def superuser_login_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_superuser:
            return view_func(request, *args, **kwargs)
        else:
            return HttpResponse("Access denied. You must be a superuser.")
    return _wrapped_view



########  for only fianance
def finance_login_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.role == 'Finance':
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponse("Access denied.You must be a finance administrator")
        else:
            # Redirect to the login page if the user is not authenticated
            return redirect('login_default')  # Change 'login_page' to your actual login URL

    return _wrapped_view


#### for recruiter
def recruiter_login_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.role == 'Recruiter':
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponse("Access denied.You must be a recruiter")
        else:
            # Redirect to the login page if the user is not authenticated
            return redirect('login_default')  # Change 'login_page' to your actual login URL

    return _wrapped_view


#################   admin panel
@superuser_login_required
def admin(request):
    users = CustomUser.objects.exclude(username=request.user.username)
    print(users)  
    return render(request,'admin.html',context={'users':users})




##############   admin panel
@superuser_login_required
def user_control(request,pk):
    users = CustomUser.objects.exclude(username=request.user.username)
    user = get_object_or_404(CustomUser, pk=pk)
   
    recruit_count = Candidate.objects.filter(user=user).count()
    finance_count = Employee.objects.filter(user=user).count()

    if request.method == 'POST' and request.POST.get('action') == 'delete':
        user.delete()
        return redirect('admin')
    return render(request,'admin.html',context={'user':user,'users':users,'recruit_count':recruit_count,'finance_count':finance_count})




from django.http import JsonResponse

@login_required(login_url='login_default')
def account(request):
    user = request.user
    return render(request,'profile.html',context={'user':user})



####### account editing 
from django.views import View
class Edit_account(LoginRequiredMixin,View):
    model = CustomUser
    success_url = reverse_lazy('profile')
    template_name = 'edit_account.html'
    login_url = 'login_default'

    def get(self, request, pk):
        user = get_object_or_404(CustomUser, pk=pk)
        return render(request, self.template_name, {'user': user})   

    def post(self, request, pk):
        user = get_object_or_404(CustomUser, pk=pk)
        
        user.username = request.POST.get("username")
        user.first_name = request.POST.get("first_name")
        user.last_name = request.POST.get("last_name")
        user.contact = request.POST.get("contact")


        user_pk = user.pk
        if CustomUser.objects.exclude(pk=user_pk).filter(username=user.username).exists():
            return HttpResponse({'User with current Username already exists'})
     
        if 'image' in request.FILES:
            user.image = request.FILES['image']

        if 'remove_image' in request.POST:
        # Remove the image associated with the user
            user.image.delete()

        user.save()

        return redirect(self.success_url)




from django.contrib.auth import update_session_auth_hash
############### delete user account and change password function
@login_required(login_url='login_default')
def manage_account(request,action):
    if action == 'delete':
        if request.method == 'POST':
            password = request.POST.get('password')
            user = authenticate(username=request.user.username, password=password)
            if user is not None:
                user.delete() 
                return JsonResponse({})
            else:
                # Password is incorrect, return an error message
                return JsonResponse({'incorrect_password': True})
            
    if action == 'change':
        if request.method == 'POST':
            password = request.POST.get('old_password')
            password2 = request.POST.get('new_password')
            user = authenticate(username=request.user.username, password=password)
            if user is not None:
                user.set_password(password2)
                user.save()

                update_session_auth_hash(request, user)
                logout(request)
                return redirect('login_default')
            else:
                # Password is incorrect, return an error message
                return HttpResponse('Invalid password')
    
    if action == 'emails':
        if request.method == 'POST':
            email = request.POST.get('email')
          
            email_exists = CustomUser.objects.filter(email=email).first()
            
            if email:
                if not email.endswith('@datapmi.com'):
                    return HttpResponse('Email format is not valid')

            if email_exists:
                return HttpResponse('Email already exists')
            
            otp = generate_otp()
            send_otp_email(email, otp)

            request.session['email'] = email
            request.session['otp'] = otp
          

            return redirect('email_change_otp')

    return render(request, 'delete_account.html')


def email_change_otp(request):
    get_email = request.session.get('email')
    if not get_email:
        return HttpResponse('Email not found in session')
    
    if request.method == 'POST':
        otp = request.POST.get('otp')
        stored_otp = request.session.get('otp')

        if otp == stored_otp: 
            user = request.user
            if user:
                user.email = get_email
                user.save()  # Save the changes to the user's email
                return redirect('profile')  # Redirect to profile page after successful email change
            else:
                return HttpResponse('User not found')  # Handle case where user is not found
        else:
            return HttpResponse('Invalid OTP')  # Handle case where OTP entered is incorrect

    return render(request, 'email_change_otp.html', {'email': get_email})








