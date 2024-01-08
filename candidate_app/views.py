from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from functools import wraps
from django.views.decorators.csrf import csrf_protect,csrf_exempt
from django.views.generic import ListView,CreateView,UpdateView,DetailView,DeleteView
from .models import Candidate,Skill
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
    


from .forms import CustomUser


def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        pass1 = request.POST.get('pass1')
        pass2 = request.POST.get('pass2')
        
        if pass1 != pass2:
            # Handle password mismatch error as needed
            return HttpResponse('Passwords are not matched')
        
        # Create CustomUser instance
        user = CustomUser(username=username, first_name=first_name, last_name=last_name,email=email)
        user.set_password(pass1)
        user.save()

        contact = request.POST.get('contact')
        image = request.FILES.get('image') 
        user.contact = contact
        user.image = image
        user.save()

        return redirect('login')  # Redirect to a success page

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
    users = CustomUser.objects.exclude(username=request.user.username)
    print(users)  
    return render(request,'admin.html',context={'users':users})



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
            # skills = request.POST.getlist("skills")
            notice_period = request.POST.get("notice_period")
            current_ctc = request.POST.get("current_ctcs")
            expected_ctc = request.POST.get("expected_ctc")
            offer_in_hands = request.POST.get("offer_in_hands")
            offer_details = request.POST.get("offer_details")
            resume = request.FILES.get("resume")
            remarks = request.POST.get("remarks")
            status = request.POST.get("status")
            additional_status = request.POST.get("client-details")
            
            
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




class Updatecandidate(UpdateView):
    model = Candidate
    success_url = reverse_lazy('list')
    template_name = 'update_candidate.html'


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


            
from django.views import View
class CheckEmailExistsView(View):
    def get(self, request, *args, **kwargs):
        email = request.GET.get('email', None)
        if email:
            email_exists = Candidate.objects.filter(email=email).exists()
            return JsonResponse({'exists': email_exists})
        else:
            return JsonResponse({'exists': False})

    


class Detailcandidate(DetailView):
    model = Candidate
    context_object_name ='detail'
    template_name = 'detail_candidate.html'
    


from django.contrib.messages.views import SuccessMessageMixin

class Deletecandidate(SuccessMessageMixin,DeleteView):
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



##### personal profile
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
    template_name = 'personal-create.html'  # Use the same template for rendering the form
    success_url = reverse_lazy('profile')


    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(ProfileCreate, self).form_valid(form)



class ProfileUpdate(LoginRequiredMixin,UpdateView):
    model = Profile
    fields = ['image']
    success_url = reverse_lazy('profile')
    template_name = 'personal-create.html'





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

class Filter(LoginRequiredMixin, ListView):
    model = Candidate
    template_name = 'search_results.html'
    context_object_name = 'users'

    def get_queryset(self):
        skills_query = self.request.GET.get('skills_search', '')
        location_query = self.request.GET.get('location_search', '')
        experience_from = self.request.GET.get('experience_from', '')
        experience_to = self.request.GET.get('experience_to', '')

        # Filter candidates based on skills
        if skills_query:
            skills = [skill.strip() for skill in skills_query.split(',')]
            q_objects = [Q(skills__name__iexact=skill) for skill in skills]
            skill_sets = [set(Candidate.objects.filter(q).values_list('id', flat=True)) for q in q_objects]
            intersection_set = set.intersection(*skill_sets)
            users = Candidate.objects.filter(id__in=intersection_set)

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
@login_required
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



def all_filter(request):
    return render(request,'filtration.html')




############# count details displayed on dashboard 

################# total count of my candidates
def mycandidates_count(request):
    if request.user.is_authenticated:
        count = Candidate.objects.filter(user=request.user).count()
        return JsonResponse({'count': count})
    else:
        return JsonResponse({'count': 0})



############# selected candidates
def selected_candidates(request):
    if request.user.is_authenticated:
        count = Candidate.objects.filter(user=request.user, status='Client Select').count()
        return JsonResponse({'count': count})
    else:
        return JsonResponse({'count': 0})



############# rejected candidates
def rejected_candidates(request):
    if request.user.is_authenticated:
        count = Candidate.objects.filter(user=request.user, status='Client Reject').count()
        return JsonResponse({'count': count})
    else:
        return JsonResponse({'count': 0})
    

############# Inprogress candidates
def inprogress_candidates(request):
    if request.user.is_authenticated:
        count = Candidate.objects.filter(user=request.user, status='').count()
        return JsonResponse({'count': count})
    else:
        return JsonResponse({'count': 0})
    


def list_of_candidates(request, status):
    if request.user.is_authenticated:
        if status == 'selected':
            candidates = Candidate.objects.filter(user=request.user, status='Client Select').all()
        elif status == 'rejected':
            candidates = Candidate.objects.filter(user=request.user, status='Client Reject').all()

        elif status == 'inprogress':
            candidates = Candidate.objects.filter(user=request.user, status='').all()

        else:
            candidates = []
        return render(request, 'selected_list.html', context={'candidates': candidates, 'status': status})



from .forms import CustomUserUpdateForm

class Edit_account(UpdateView):
    model = CustomUser
    form_class = CustomUserUpdateForm
    template_name = 'edit_account.html'
    success_url = reverse_lazy('profile')

    def get_object(self, queryset=None):
        return get_object_or_404(CustomUser, pk=self.request.user.pk)


    
    


################ delete user account
@login_required
def delete_account(request):
    if request.method == 'POST':
        password = request.POST.get('password')
        user = authenticate(username=request.user.username, password=password)
        if user is not None:
            # Password is correct, delete the account
            user.delete()
            messages.success(request, 'Your account has been deleted.')
            return JsonResponse({})
        else:
            # Password is incorrect, return an error message
            return JsonResponse({'incorrect_password': True})
    else:
        return render(request, 'delete_account.html')




############ for admin dashboard page details
# def admin_dashboard(request):
#     users = CustomUser.objects.all()
#     print(users)  
#     return render(request,'admin.html',context={'users':users})














