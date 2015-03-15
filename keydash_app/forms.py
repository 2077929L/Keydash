from django import forms
from keydash_app.models import UserProfile
from django.contrib.auth.models import User

class UserForm(forms.ModelForm):
    # password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('email',)

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('picture',)