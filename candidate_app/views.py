from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from functools import wraps
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView,CreateView,UpdateView,DetailView,DeleteView
from .models import Candidate,Skill
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import CustomUser
from .utils import generate_otp, send_otp_email
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .utils import send_recovery_link



##### registration
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
            return redirect('login_default')
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
                reset_link = f"http://127.0.0.1:8000/reset_password/{token}/"

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
        # Verify the token
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


### for recruiter
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



@superuser_login_required
def admin(request):
    users = CustomUser.objects.exclude(username=request.user.username)
    print(users)  
    return render(request,'admin.html',context={'users':users})



@superuser_login_required
def user_control(request,pk):
    users = CustomUser.objects.exclude(username=request.user.username)
    user = get_object_or_404(CustomUser, pk=pk)
    if request.method == 'POST' and request.POST.get('action') == 'delete':
        user.delete()
        return redirect('admin')
    return render(request,'admin.html',context={'user':user,'users':users})




@recruiter_login_required
def user(request):
    return render(request,'user.html')



from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

############  this is only for personal crud operations

class ListCandidate(LoginRequiredMixin,ListView):
    model = Candidate
    fields = "__all__"
    template_name = 'mycandidates.html'
    context_object_name = "list"
    login_url = 'login_default'

    @method_decorator(recruiter_login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


    def get_queryset(self):
        # Filter the queryset based on the logged-in user
        queryset = super().get_queryset().filter(user=self.request.user)
        return queryset




class Createcandidate(LoginRequiredMixin,CreateView):
    template_name = 'add_candidate.html'
    success_url = reverse_lazy('list')
    login_url = 'login_default'

    @method_decorator(recruiter_login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request):
        return render(request, self.template_name)      

    def post(self, request):
        if request.method == "POST":
            
            designation = request.POST.get("designation")
            client_name = request.POST.get("client_name")
            mode_of_work = request.POST.get("mode_of_work_1")
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
            notice_period = request.POST.get("notice_period")
            current_ctc = request.POST.get("current_ctcs")
            expected_ctc = request.POST.get("expected_ctc")
            offer_in_hands = request.POST.get("offer_in_hands")
            offer_details = request.POST.get("offer_details")
            resume = request.FILES.get("resume")
            remarks = request.POST.get("remarks")
            status = request.POST.get("status")
            additional_status = request.POST.get("client-details")

            if Candidate.objects.filter(email=email).exists():
                return HttpResponse({'Candidate with current Email address already exists'})
            
            
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
                notice_period=notice_period,
                current_ctc=current_ctc,
                expected_ctc=expected_ctc,
                offer_in_hands=offer_in_hands,
                offer_details=offer_details,
                resume=resume,
                status=status,
                additional_status=additional_status,
                user=request.user
            )
            candidate.save()

            

            try:    
                skill_names = request.POST.getlist("skills")
                skills = [Skill.objects.get_or_create(name=skill_name, user=request.user)[0] for skill_name in skill_names]
                candidate.skills.set(skills)
            
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

    


from .forms import CandidateUpdateForm
from django.shortcuts import get_object_or_404



class Updatecandidate(LoginRequiredMixin,UpdateView):
    model = Candidate
    success_url = reverse_lazy('list')
    template_name = 'update_candidate.html'
    login_url = 'login_default'

    @method_decorator(recruiter_login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


    def get(self, request, pk):
        candidate = get_object_or_404(Candidate, pk=pk, user=request.user)
        return render(request, self.template_name, {'candidate': candidate})   

    def post(self, request, pk):
        if pk is None:
            # Creating a new candidate
                candidate = Candidate(user=request.user)
        else:
            # Updating an existing candidate
            candidate = get_object_or_404(Candidate, pk=pk, user=request.user)
        
        candidate.designation = request.POST.get("designation")
        candidate.client_name = request.POST.get("client_name")
        candidate.mode_of_work = request.POST.get("mode_of_works")
        candidate.first_name = request.POST.get("first_name")
        candidate.last_name = request.POST.get("last_name")
        candidate.email = request.POST.get("email")
        candidate.phone = request.POST.get("phone")
        candidate.gender = request.POST.get("gender")
        candidate.location = request.POST.get("location")
        candidate.college = request.POST.get("college")
        candidate.qualification = request.POST.get("qualification")
        candidate.graduation_year = request.POST.get("graduation_year")
        candidate.current_company = request.POST.get("current_company")
        candidate.experience = request.POST.get("experience")
        candidate.relevent_experience = request.POST.get("relevent_experience")
        candidate.notice_period = request.POST.get("notice_period")
        candidate.current_ctc = request.POST.get("current_ctcs")
        candidate.expected_ctc = request.POST.get("expected_ctc")
        candidate.offer_in_hands = request.POST.get("offer_in_hands")
        candidate.offer_details = request.POST.get("offer_details")
        candidate.remarks = request.POST.get("remarks")
    
        candidate.status = request.POST.get("status")
        candidate.additional_status = request.POST.get("client-details")
      
        new_resume = request.FILES.get('new_resume')
        keep_resume = request.POST.get('keep_resume')


        candidate_pk = candidate.pk

        if Candidate.objects.exclude(pk=candidate_pk).filter(email=candidate.email).exists():
            return HttpResponse({'Candidate with current Email address already exists'})


        if not keep_resume and new_resume:
            candidate.resume = new_resume

        candidate.save()

        try:
            skill_names = request.POST.getlist("skills")

            skill_names = [name.strip() for name in skill_names if name.strip()]

            if skill_names:
            # Skills provided in the request, update the candidate's skills
                new_skills = [Skill.objects.get_or_create(name=skill_name, user=request.user)[0] for skill_name in skill_names]
                candidate.skills.set(new_skills)

            # Handle resume update
            new_resume = request.FILES.get('new_resume')
            keep_resume = request.POST.get('keep_resume')
            if not keep_resume and new_resume:
                candidate.resume = new_resume

            # Save the candidate
            candidate.save()

            return redirect(self.success_url)

        except Exception as e:
            # Log the error for debugging
            print(f"Error saving candidate: {e}")
            # Return an error response
            return render(request, self.template_name, {'error': 'Error: Could not save the candidate.'})


             
class Detailcandidate(LoginRequiredMixin,DetailView):
    model = Candidate
    context_object_name ='detail'
    template_name = 'detail_candidate.html'
    login_url = 'login_default'

    @method_decorator(recruiter_login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    



@recruiter_login_required
def delete_candidate(request, pk):
    candidate = get_object_or_404(Candidate, pk=pk)

    if request.method == 'POST':
        candidate.delete()
        return redirect('list')

    return render(request, 'delete_candidate.html', {'candidate': candidate})




#### logout
def signout(request):
    logout(request)
    return redirect('login_default')



class Allcandidates(LoginRequiredMixin,ListView):
    model = Candidate
    fields = ['email','phone','first_name','last_name','alt_phone','sex','qualification','skills','experience','designation','expected_ctc','current_ctc','availability','notice_period','current_company','location','resume','remarks','updated_by','updated_on']
    template_name = 'allcandidates.html'
    context_object_name = "all"
    login_url = 'login_default'

    @method_decorator(recruiter_login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    



##### personal profile (account settings info)
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
        user.email = request.POST.get("email")
        user.contact = request.POST.get("contact")


        user_pk = user.pk
        if CustomUser.objects.exclude(pk=user_pk).filter(username=user.username).exists():
            return HttpResponse({'User with current Username already exists'})
        
        if CustomUser.objects.exclude(pk=user_pk).filter(email=user.email).exists():
            return HttpResponse({'User with current Email address already exists'})

        if user.email:
            if not user.email.endswith('@datapmi.com'):
                return HttpResponse('Email format is not valid')

        # Handle the image file
        if 'image' in request.FILES:
            user.image = request.FILES['image']

        if 'remove_image' in request.POST:
        # Remove the image associated with the user
            user.image.delete()

        user.save()

        return redirect(self.success_url)





from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin

########### autocomplete recommendation using AJAX for email id filtration
from django.http import JsonResponse
def autocomplete_username(request):
    if 'term' in request.GET:
        term = request.GET.get('term')
        users = Candidate.objects.filter(email__istartswith=term)
        suggestions = [{'label': user.email, 'value': user.id} for user in users]
        return JsonResponse({'suggestions': suggestions}, safe=False)
    return JsonResponse({'suggestions': []})




##### filter only for skills and locations
from django.db.models.query import Q
from django.http import HttpResponse
from django.views.generic import ListView
from django.db.models import Q
from .models import Candidate, Skill
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.db.models import Count

class Filter(LoginRequiredMixin, ListView):
    model = Candidate
    template_name = 'search_results.html'
    context_object_name = 'users'
    login_url = 'login_default'

    @method_decorator(recruiter_login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


    def get_queryset(self):
        skills_query = self.request.GET.get('skills_search', '')
        location_query = self.request.GET.get('location_search', '')
        experience_from = self.request.GET.get('experience_from', '')
        experience_to = self.request.GET.get('experience_to', '')

        # Start with all candidates
        users = Candidate.objects.all()

        if skills_query:
            skills = [skill.strip() for skill in skills_query.split(',')]

            for skill in skills:
                users = users.filter(skills__name__iexact=skill)

            
            # Check if the queryset is empty
            if not users.exists():
                return HttpResponse("No results found for skills", status=200)

        else:
            users = Candidate.objects.all()

        # Filter candidates based on location
        if location_query:
            users = users.filter(location__icontains=location_query)

            # Check if the queryset is empty
            if not users.exists():
                return HttpResponse("No results found for location", status=200)

        # Filter candidates based on experience
        if experience_from and experience_to:
            users = users.filter(experience__range=(float(experience_from), float(experience_to)))
        elif experience_from:
            users = users.filter(experience__gte=float(experience_from))
        elif experience_to:
            users = users.filter(experience__lte=float(experience_to))

        print(users.query)  # Print the generated SQL query to the console
        return users


## suggession for getting skills 
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_GET


############# autocomplete for skills filter
@require_GET
def autocomplete_skills(request):
    term = request.GET.get('term', '')
    skills = Skill.objects.filter(name__istartswith=term).values('name').distinct()
    suggestions = [{'label': skill['name'], 'value': skill['name']} for skill in skills]
    return JsonResponse({'suggestions': suggestions}, safe=False)




############## autocomplete for location filter
def autocomplete_locations(request):
    if 'term' in request.GET:
        term = request.GET.get('term')
        locations = Candidate.objects.filter(location__icontains=term).values('location')
        suggestions = list(locations.values_list('location', flat=True))
        return JsonResponse({'suggestions': suggestions}, safe=False)

    return JsonResponse({'suggestions': []})


@recruiter_login_required
def all_filter(request):
    return render(request,'filtration.html')




############# count details displayed on dashboard 

################# total count of all candidates
@recruiter_login_required
def totalcandidates_count(request):
    if request.user.is_authenticated:
        count = Candidate.objects.all().count()
        return JsonResponse({'count': count})
    else:
        return JsonResponse({'count': 0})


################# total count of my candidates
@recruiter_login_required
def mycandidates_count(request):
    if request.user.is_authenticated:
        count = Candidate.objects.filter(user=request.user).count()
        return JsonResponse({'count': count})
    else:
        return JsonResponse({'count': 0})



############# selected candidates
@recruiter_login_required
def selected_candidates(request):
    if request.user.is_authenticated:
        count = Candidate.objects.filter(user=request.user, status='Client Select').count()
        return JsonResponse({'count': count})
    else:
        return JsonResponse({'count': 0})



############# rejected candidates
@recruiter_login_required
def rejected_candidates(request):
    if request.user.is_authenticated:
        count = Candidate.objects.filter(user=request.user, status='Client Reject').count()
        return JsonResponse({'count': count})
    else:
        return JsonResponse({'count': 0})
    

############# Inprogress candidates
@recruiter_login_required
def inprogress_candidates(request):
    if request.user.is_authenticated:
        count = Candidate.objects.filter(user=request.user, status='Interview Ongoing').count()
        return JsonResponse({'count': count})
    else:
        return JsonResponse({'count': 0})
    

@recruiter_login_required
def saved_candidates(request):
    if request.user.is_authenticated:
        count = Candidate.objects.filter(user=request.user, status='Store Data').count()
        return JsonResponse({'count': count})
    else:
        return JsonResponse({'count': 0})



@recruiter_login_required
def list_of_candidates(request, status):
    if request.user.is_authenticated:
        if status == 'selected':
            heading = 'Selected Candidates'
            candidates = Candidate.objects.filter(user=request.user, status='Client Select').all()
        elif status == 'rejected':
            heading = 'Rejected Candidates'
            candidates = Candidate.objects.filter(user=request.user, status='Client Reject').all()

        elif status == 'inprogress':
            heading = 'Inprogress Candidates'
            candidates = Candidate.objects.filter(user=request.user, status='Interview Ongoing').all()

        elif status == 'saved':
            heading = 'Saved Candidates'
            candidates = Candidate.objects.filter(user=request.user, status='Store Data').all()

        else:
            candidates = []
        return render(request, 'selected_list.html', context={'candidates': candidates, 'status': status,'heading':heading})




from django.contrib.auth import update_session_auth_hash

############### delete user account and change password function
@login_required(login_url='login_default')
def manage_account(request,action):
    if action == 'delete':
        if request.method == 'POST':
            password = request.POST.get('password')
            user = authenticate(username=request.user.username, password=password)
            if user is not None:
                # Password is correct, delete the account
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

    return render(request, 'delete_account.html')





###### get skills from skills.txt
def get_skills(request):
    # Fetch skills from the Skill model
    skills_from_database = Skill.objects.values_list('name', flat=True)

    # Fetch skills from the text file
    with open('candidate_app/static/skills.txt', 'r') as file:
        skills_from_file = [line.strip() for line in file if line.strip()]

    # Combine skills from both sources
    all_skills = list(set(skills_from_database) | set(skills_from_file))

    # Return the combined skills as a JSON response
    return JsonResponse({'skills': all_skills})
    




################## Finance team section
from .models import Employee

@finance_login_required
def finance_dashboard(request):
    return render(request,'finance/finance_dashboard.html')



@finance_login_required
def add_employee(request):
     
     if request.method == 'POST':
        name=request.POST.get('name')
        email=request.POST.get('email')
        mobile=request.POST.get('mobile')
        alternate=request.POST.get('alternate')
        position=request.POST.get('position')
        clientName=request.POST.get('clientName')
        clientLocation=request.POST.get('clientLocation')
        projectDirector=request.POST.get('projectDirector')
        projectPartner=request.POST.get('projectPartner')
        fees=request.POST.get('fees')
        active_inactive = request.POST.get('active_inactive')
        employeeStatus=request.POST.get('employeeStatus')
        joiningDate=request.POST.get('joiningDate')
        lastWorkingDate=request.POST.get('lastWorkingDate')
        workOrderStartDate=request.POST.get('workOrderStartDate')
        workOrderEndDate=request.POST.get('workOrderEndDate')
        woDetail=request.POST.get('woDetail')
        uploadWorkOrder=request.FILES.get('uploadWorkOrder')
        uploadNDA=request.FILES.get('uploadNDA')
        uploadResume=request.FILES.get('uploadResume')

        if Employee.objects.filter(email=email).exists():
                return HttpResponse({'Employee with current Email address already exists'})

        employee = Employee(user=request.user,
                            name=name,
                            email=email,
                            mobile=mobile,
                            alt_mobile=alternate,
                            position=position,
                            client_name=clientName,
                            client_location=clientLocation,
                            project_director=projectDirector,
                            project_partner=projectPartner,
                            fees=fees,
                            active_inactive = active_inactive,
                            employee_status=employeeStatus,
                            joining_date=joiningDate,
                            last_working_date=lastWorkingDate,
                            start_date_of_work_order=workOrderStartDate,
                            end_date_of_work_order=workOrderEndDate,
                            work_order_detail=woDetail,
                            upload_work_order=uploadWorkOrder,
                            upload_nda=uploadNDA,
                            upload_resume=uploadResume)
        
        employee.save()

        return redirect('finance_dashboard')
     
     return render(request,'finance/add_employee.html')



from django.db import IntegrityError

class Updateemployee(LoginRequiredMixin,UpdateView):
    model = Employee
    success_url = reverse_lazy('all_employee')
    template_name = 'finance/update_employee.html'
    login_url = 'login_default'

    @method_decorator(finance_login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, pk):
        employee = get_object_or_404(Employee, pk=pk, user=request.user)
        return render(request, self.template_name, {'employee': employee})   

    def post(self, request, pk):
        if pk is None:
            # Creating a new candidate
            employee = Employee(user=request.user)
        else:
            # Updating an existing candidate
            employee = get_object_or_404(Employee, pk=pk, user=request.user)
        
        employee.name = request.POST.get("name")
        employee.email = request.POST.get("email")
        employee.mobile = request.POST.get("mobile")
        employee.alt_mobile = request.POST.get("alternate")
        employee.position = request.POST.get("position")
        employee.client_name = request.POST.get("clientName")
        employee.client_location = request.POST.get("clientLocation")
        employee.project_director = request.POST.get("projectDirector")
        employee.project_partner = request.POST.get("projectPartner")
        employee.fees = request.POST.get("fees")
        employee.active_inactive = request.POST.get("active_inactive")
        employee.employee_status = request.POST.get("employeeStatus")
        employee.joining_date = request.POST.get("joiningDate")
        employee.last_working_date = request.POST.get("lastWorkingDate")
        employee.start_date_of_work_order = request.POST.get("workOrderStartDate")
        employee.end_date_of_work_order = request.POST.get("workOrderEndDate")
        employee.work_order_detail = request.POST.get("woDetail")
        
        # new_resume = request.FILES.get('new_resume')
        # keep_resume = request.POST.get('keep_resume')

        employee_pk = employee.pk

        if Employee.objects.exclude(pk=employee_pk).filter(email=employee.email).exists():
            return HttpResponse({'Employee with current Email address already exists'})
        
        employee.save()
        
        try:

            upload_work_order = request.FILES.get('uploadWorkorder')
            keep_workorder = request.POST.get('keep')
            if not keep_workorder and upload_work_order:
                employee.upload_work_order = upload_work_order

            upload_nda = request.FILES.get('uploadNDA')
            keep_nda = request.POST.get('keep')
            if not keep_nda and upload_nda:
                employee.upload_nda = upload_nda

            new_resume = request.FILES.get('uploadResume')
            keep_resume = request.POST.get('keep_resume')
            if not keep_resume and new_resume:
                employee.upload_resume = new_resume

            employee.save()
            return redirect(self.success_url)

        except IntegrityError as e:
            if 'email' in str(e):
                error_message = 'An employee with this email already exists.'
            else:
                error_message = 'An error occurred while saving the employee.'
            return render(request, self.template_name, {'employee': employee, 'error_message': error_message})



@finance_login_required
def all_employee(request):
    employees = Employee.objects.all().order_by('-joining_date')
    return render(request,'finance/all_employee.html',context={'employees':employees})



@finance_login_required
def detail_employee(request,pk):
    employees = Employee.objects.get(id=pk)
    return render(request,'finance/detail_employee.html',context={'detail':employees})


from django.db.models import F
from datetime import date,timedelta
########### display 5 employee have contract end date is approaching
def end_work_order(request):
    today = date.today()
    employees = Employee.objects.annotate(
        days_until_end=F('end_date_of_work_order') - today
    ).order_by('days_until_end')[:5]

    employee_names = [employee.name for employee in employees]
    return JsonResponse({'employee_names': employee_names})





from django.core.management.base import BaseCommand
from .utils import send_notification
############# email sending to user before 15 days of end work date
class Command(BaseCommand):
    help = 'Notify users 15 days before their contract end date'

    def handle(self, *args, **kwargs):
        # Get today's date
        today = timezone.now().date()

        # Calculate the date 15 days from now
        notification_date = today + timedelta(days=15)

        # Get employees whose contract end date is equal to the notification date
        employees_to_notify = Employee.objects.filter(end_date_of_work_order=notification_date)

        finance_user = CustomUser.objects.get(role='Finance')

        for employee in employees_to_notify:
            self.send_notification(finance_user.email, employee.name)






