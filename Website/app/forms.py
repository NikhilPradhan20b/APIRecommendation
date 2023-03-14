from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UsernameField ,PasswordChangeForm
from django.contrib.auth.models import User
from django.utils.translation import gettext, gettext_lazy as _
from django.contrib.auth import password_validation
from .models import customer, Comment
class CustomerRegistrationForm(UserCreationForm):
    password1 = forms.CharField(label='password',widget=forms.PasswordInput(attrs={'class':'form-control'}))
    password2 = forms.CharField(label='Confirm Password (again)',widget=forms.PasswordInput(attrs={'class':'form-control'}))
    email = forms.CharField(required=True, widget=forms.EmailInput(attrs={'class':'form-control'}))
    class Meta:
        model = User
        fields =['username','email','password1','password2']
        label = {'email':'Email'}
        widgets ={'username': forms.TextInput(attrs={'class':'form-control'})}

class LoginForm(AuthenticationForm):
    username = UsernameField(widget=forms.TextInput(attrs={'autofocus':True, 'class':'form-control'}))
    password = forms.CharField(label=_("password"),strip=False,widget=forms.PasswordInput(attrs={'autocomplete':'current-password', 'class':'form-control'}))

class MyPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(label=_("old password"), strip=False, widget=forms.PasswordInput(attrs={'autocomplete': 'current-password','autofocus': True,'class':'form-control'}))
    new_password1 = forms.CharField(label=_("New password"), strip=False, widget=forms.PasswordInput(attrs={'autocomplete': 'new-password','class':'form-control'}),help_text=password_validation.password_validators_help_text_html())
    new_password2 = forms.CharField(label=_("Confirm New Password"), strip=False, widget=forms.PasswordInput(attrs={'autocomplete': 'new-password','class':'form-control'}))

class CustomerProfileForm(forms.ModelForm):
    class Meta:
        model = customer
        fields =['name','address']
        widgets = {'name':forms.TextInput(attrs={'class':'form-control'}),'address':forms.TextInput(attrs={'class':'form-control'})}


class CommentForm(forms.ModelForm):
    subject = forms.CharField(max_length=255)
    comment = forms.CharField(widget=forms.Textarea)
    rating = forms.IntegerField()
    class Meta:
        model = Comment
        fields = ["subject","comment","rating"]

