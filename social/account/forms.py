from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from .models import Profile


class UserRegistrationForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    def clean_email(self):
        ''' To avoid same email for each user'''
        email = self.cleaned_data['email']
        user = User.objects.filter(email=email).exists()
        if user:
            raise ValidationError('This user already exist.')
        return email

    def clean_username(self):
        ''' To avoid same username'''
        username = self.cleaned_data['username']
        user = User.objects.filter(username=username).exists()
        if user:
            raise ValidationError('This user already exist.')
        return username

    def clean(self):
        ''' check password and confirm password'''
        cd = super().clean()
        p1 = cd.get('password1')
        p2 = cd.get('password2')

        if p1 and p2 and p1 != p2:
            raise ValidationError('Passwords must match!')


class UserLoginForm(forms.Form):
    username = forms.CharField(label='Username / Email', widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))


class EditUserForm(forms.ModelForm):
    '''we are using to different models, and Profile model has no attr named email.
    so we use email as class_var'''
    email = forms.EmailField()

    class Meta:
        model = Profile
        fields = ('age', 'bio')
