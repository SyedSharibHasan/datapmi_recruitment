
from django import forms
from .models import Candidate

class CandidateForm(forms.ModelForm):
    class Meta:
        model = Candidate
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['resume'].required = False





from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser


class CustomUserForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'email', 'contact']




####filter
class SkillSearchForm(forms.Form):
    skills_search = forms.CharField(label='Search skillsets', max_length=100)



class CandidateUpdateForm(forms.ModelForm):
    class Meta:
        model = Candidate
        fields = '__all__'    



from .models import Profile

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']