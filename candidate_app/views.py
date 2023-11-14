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


from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

############  this is only for personal crud operations
@method_decorator(login_required, name='dispatch')
class ListCandidate(ListView):
    model = Candidate
    fields = "__all__"
    template_name = 'mycandidates.html'
    context_object_name = "list"


    def get_queryset(self):
        # Filter the queryset based on the logged-in user
        queryset = super().get_queryset().filter(user=self.request.user)
        return queryset



@method_decorator(login_required, name='dispatch')
class Createcandidate(CreateView):

    template_name = 'add_candidate.html'
    success_url = reverse_lazy('list')
    
    def get(self, request):
        return render(request, self.template_name)      

    def post(self, request):
        if request.method == "POST":
            
        
            designation = request.POST.get("designation")
            client_name = request.POST.get("client_name")
            mode_of_work = request.POST.get("mode_of_work")
            first_name = request.POST.get("first_name")
            last_name = request.POST.get("last_name")
            email = request.POST.get("email")
            phone = request.POST.get("phone")
            gender = request.POST.get("gender")
            location = request.POST.get("location")
            college = request.POST.get("college")
            qualification = request.POST.get("qualification")
            graduation_year = request.POST.get("graduation_year")
            current_company = request.POST.get("current_company")
            experience = request.POST.get("experience")
            relevent_experience = request.POST.get("relevent_experience")
            skills = request.POST.get("skills")
            notice_period = request.POST.get("notice_period")
            current_ctc = request.POST.get("current_ctc")
            expected_ctc = request.POST.get("expected_ctc")
            offer_in_hands = request.POST.get("offer_in_hands")
            offer_details = request.POST.get("offer_details")
            resume = request.POST.get("resume")
            remarks = request.POST.get("remarks")
            recruiter = request.POST.get("recruiter")
            screening_time = request.POST.get("screening_time")
            status = request.POST.get("status")
            rejection_reason = request.POST.get("rejection_reason")
            additional_status = request.POST.get("additional_status")
            rejection_reason_for_r1_r4 = request.POST.get("rejection_reason_for_r1-r4")
            additional_status = request.POST.get("additional_status")
            offer = request.POST.get("offer")
            offer_reject_reason = request.POST.get("offer_reject_reason")
            
            
            # Create a new Candidate object with the retrieved data
            candidate = Candidate(
                
                designation=designation,
                client_name=client_name,
                mode_of_work=mode_of_work,
                first_name=first_name,
                last_name=last_name,
                email=email,
                phone=phone,
                gender=gender,
                location=location,
                college=college,
                qualification=qualification,
                graduation_year = graduation_year,
                current_company=current_company,
                remarks=remarks,
                experience=experience,
                relevent_experience=relevent_experience,
                skills=skills,
                notice_period=notice_period,
                current_ctc=current_ctc,
                expected_ctc=expected_ctc,
                offer_in_hands=offer_in_hands,
                offer_details=offer_details,
                resume=resume,
                recruiter=recruiter,
                screening_time=screening_time,
                status=status,
                rejection_reason=rejection_reason,
                additional_status=additional_status,
                rejection_reason_for_r1_r4=rejection_reason_for_r1_r4,
                offer = offer,
                offer_reject_reason=offer_reject_reason,
                user=request.user
            )

            try:
                # Save the new candidate to the database
                candidate.save()
                # Redirect to a success page
                return redirect(self.success_url)
            except Exception as e:
                # Log the error for debugging
                print(f"Error saving candidate: {e}")
                # Return an error response
                return render(request, self.template_name, {'error': 'Error: Could not save the candidate.'})

        
        
    def form_valid(self, form):
        # Set the user before saving the form
        form.instance.user = self.request.user
        return super().form_valid(form)

    





  



# class Updatecandidate(UpdateView):
#     model = Candidate
#     success_url= reverse_lazy('list')
#     template_name = 'add_candidate.html'
#     fields = "__all__"
    

@method_decorator(login_required, name='dispatch')
class Updatecandidate(UpdateView):
    model = Candidate
    template_name = 'update_candidate.html'  # Create this template for the update form
    fields = ['designation', 'client_name', 'mode_of_work']  # Add other fields as needed
    success_url = reverse_lazy('list')

    def get_queryset(self):
        # Filter the queryset based on the logged-in user
        queryset = super().get_queryset().filter(user=self.request.user)
        return queryset


    
    


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