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




# def main(request):
#     if request.user.is_superuser:
#         # Redirect superuser to admin.html
#         return render(request,'admin.html')
#     else:
#         # Redirect normal user to user.html
#         return render(request,'user.html')
    


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
                return redirect('admin')  # Redirect to the admin page
            else:
                # Redirect normal user to user.html
                login(request, user)
                return redirect('user')  # Redirect to the user page
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
    # candidate = Candidate.objects.all()
    return render(request,'user.html')


############  this is only for personal crud operations
class ListCandidate(ListView):
    model = Candidate
    fields = ['email','phone','first_name','last_name','alt_phone','sex','qualification','skills','experience','designation','expected_ctc','current_ctc','availability','notice_period','current_company','location','resume','remarks','updated_by','updated_on']
    template_name = 'mycandidates.html'
    context_object_name = "list"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['list'] = context['list'].filter(user=self.request.user)
        return context


class Createcandidate(CreateView):
    model = Candidate
    success_url= reverse_lazy('list')
    template_name = 'add_candidate.html'
    fields = ['email','phone','first_name','last_name','alt_phone','sex','qualification','skills','experience','designation','expected_ctc','current_ctc','availability','notice_period','current_company','location','resume','remarks','updated_by',]

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(Createcandidate, self).form_valid(form)


class Updatecandidate(UpdateView):
    model = Candidate
    success_url= reverse_lazy('list')
    template_name = 'add_candidate.html'
    fields = ['email','phone','first_name','last_name','alt_phone','sex','qualification','skills','experience','designation','expected_ctc','current_ctc','availability','notice_period','current_company','location','resume','remarks','updated_by']


class Detailcandidate(DetailView):
    model = Candidate
    context_object_name ='detail'
    template_name = 'detail_candidate.html'



class Deletecandidate(DeleteView):
    model = Candidate
    # context_object_name = 'task'
    success_url = reverse_lazy('list')
    template_name = 'delete_candidate.html'
    success_message = 'Deleted succesfully'



def signout(request):
    logout(request)
    return redirect('login')



class Allcandidates(ListView):
    model = Candidate
    fields = ['email','phone','first_name','last_name','alt_phone','sex','qualification','skills','experience','designation','expected_ctc','current_ctc','availability','notice_period','current_company','location','resume','remarks','updated_by','updated_on']
    template_name = 'allcandidates.html'
    context_object_name = "all"




#### dashboard
def dashboard(request):
    return render(request,'dashboard.html')



#####cpersonal profile
from .models import Profile
from django.http import JsonResponse

class ProfileList(ListView):
    model = Profile
    fields="__all__"
    context_object_name = 'profile'
    template_name='profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = context['profile'].filter(user=self.request.user)
        return context





class ProfileCreate(CreateView):
    model = Profile
    fields = ['image']
    template_name = 'profile.html'  # Use the same template for rendering the form

    def form_valid(self, form):
        form.instance.user = self.request.user
        response_data = {
            'success': True,
            'message': 'Profile created successfully.'
        }
        return JsonResponse(response_data)












###### search 