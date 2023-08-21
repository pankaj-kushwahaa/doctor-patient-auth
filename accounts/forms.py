from django import forms
from .models import User
from django.contrib.auth.forms import AuthenticationForm, UserChangeForm, UsernameField, PasswordChangeForm, UserCreationForm
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator


class RegisterForm(UserCreationForm):
  password1 = forms.CharField(max_length=100, label="Password", widget=forms.PasswordInput(attrs={'class':'form-control'}), error_messages={'required':'Password is required'})
  password2 = forms.CharField(max_length=100, label="Confirm Password", widget=forms.PasswordInput(attrs={'class':'form-control'}), error_messages={'required': 'Confirm Password is required'})

  class Meta:
    model = User
    fields = ['email', 'username', 'first_name', 'last_name', 'profile_pic', 'address','city', 'state', 'pincode', 'user_type', 'password1', 'password2']
    labels = {'profile_pic':"Profile Picture", 'pincode':"Pin Code"}
    widgets = {
      'email' : forms.EmailInput(attrs={'class':'form-control', "autofocus": ""}),
      'username' : forms.TextInput(attrs={'class':'form-control'}),
      'first_name': forms.TextInput(attrs={'class':'form-control'}),
      'last_name': forms.TextInput(attrs={'class':'form-control'}),
      'profile_pic': forms.FileInput(attrs={'class':'form-control'}),
      'address': forms.TextInput(attrs={'class':'form-control'}),
      'city': forms.TextInput(attrs={'class':'form-control'}),
      'state': forms.Select(attrs={'class':'form-select'},),
      'pincode': forms.NumberInput(attrs={'class':'form-control', 'min':'100000', 'max':'999999'}),
      'user_type': forms.Select(attrs={'class':'form-select'}),
    }
    help_texts = {
      'email': 'Enter your email',
      'username': 'Enter your username, username should be unique',
      'password1' : 'Enter your password'
    }
    error_messages = {
      'email': {'required': 'Email is required', 'invalid': 'Please enter a valid email'},
      'username': {'required': 'Username is required', 'max_length': 'Username is too long'},
      'password1':{'required': 'Password is required', 'invalid': ''}, 
    }
  
  def clean_password2(self):
    # Check that the two password entries match
    password1 = self.cleaned_data.get("password1")
    password2 = self.cleaned_data.get("password2")
    if password1 and password2 and password1 != password2:
      raise ValidationError("Passwords don't match")
    return password2
  

  # Override the save method of ModelForm. Save the provided password in hashed format
  def save(self, commit=True):
    user = super().save(commit=False)
    user.set_password(self.cleaned_data["password1"])
    if commit:
      user.save()
    return user
    

class LoginForm(AuthenticationForm):
  username = UsernameField(widget=forms.EmailInput(attrs={"autofocus": True, 'class':'form-control',}), required=True, validators=[EmailValidator], error_messages={'required':'Email address is required'})
  password = forms.CharField(label=_("Password"), strip=False, widget=forms.PasswordInput(attrs={'class':'form-control'}), required=True, error_messages={'required':'Password is required'})


class ChangePasswordForm(PasswordChangeForm):
  old_password = forms.CharField(label=_("Old password"), strip=False, widget=forms.PasswordInput(attrs={"autocomplete": "current-password", "autofocus": True, 'class':'form-control'}),)
  new_password1 = forms.CharField(label=_("New password"), widget=forms.PasswordInput(attrs={"autocomplete": "new-password", 'class':'form-control'}),strip=False,)
  new_password2 = forms.CharField(label=_("New password confirmation"), strip=False, widget=forms.PasswordInput(attrs={"autocomplete": "new-password", 'class':'form-control'}),)


class ChangeProfileForm(forms.ModelForm): 
  class Meta:
    model = User
    fields = ['first_name', 'last_name', 'profile_pic', 'address','city', 'state', 'pincode']
    labels = {'profile_pic':"Profile Picture", 'pincode':"Pin Code"}
    widgets = {
      'first_name': forms.TextInput(attrs={'class':'form-control', "autofocus": True}),
      'last_name': forms.TextInput(attrs={'class':'form-control'}),
      'profile_pic': forms.FileInput(attrs={'class':'form-control'}),
      'address': forms.TextInput(attrs={'class':'form-control'}),
      'city': forms.TextInput(attrs={'class':'form-control'}),
      'state': forms.Select(attrs={'class':'form-control'}),
      'pincode': forms.NumberInput(attrs={'class':'form-control',  'min':'100000', 'max':'999999'}),
    }
  
  # def clean_pincode(self):
  #   print("clean_pincode() is called")
  #   pin = self.cleaned_data.get('pincode')
  #   print("pincode value:",pin, type(pin))
    
  #   if pin < 100000 and pin > 999999:
  #     raise ValidationError("Pin Code is not valid")
  #   return pin