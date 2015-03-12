class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('picture')