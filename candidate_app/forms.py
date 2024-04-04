
from django import forms
from .models import Candidate

class CandidateForm(forms.ModelForm):
    class Meta:
        model = Candidate
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['resume'].required = False




####  filter
class SkillSearchForm(forms.Form):
    skills_search = forms.CharField(label='Search skillsets', max_length=100)



class CandidateUpdateForm(forms.ModelForm):
    class Meta:
        model = Candidate
        fields = '__all__'    



from django import forms
from .models import CustomUser

class CustomUserUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'email', 'contact', 'image']





