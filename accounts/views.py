from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .forms import RegisterForm, LoginForm, ChangePasswordForm, ChangeProfileForm
from django.contrib.auth.forms import UserCreationForm

class Register(View):
  def get(self, request):
    form = RegisterForm(initial={'state':'Select State'})
    context = dict(form=form)
    return render(request, 'accounts/register.html', context)

  def post(self, request):
    form = RegisterForm(request.POST, request.FILES)
    if form.is_valid():
      form.save()
      messages.success(request, 'Registered successfully')
      return redirect('login')
    context = dict(form=form)
    return render(request, 'accounts/register.html', context)

class Login(View):
  def get(self, request):
    form = LoginForm()
    context = dict(form=form)
    return render(request, 'accounts/login.html', context)

  def post(self, request):
    form = LoginForm(request=request, data=request.POST)
    if form.is_valid():
      email = form.cleaned_data['username']
      password = form.cleaned_data['password']
      print("inside")
      user = authenticate(request, username=email, password=password)
      print(user)
      if user is not None:
        login(request, user)
        messages.success(request, 'User logged in')
        return redirect('dashboard')
    context = dict(form=form)
    print("after")
    return render(request, 'accounts/login.html', context)
  
@method_decorator(login_required, name='dispatch')
class ProfileChange(View):
  def get(self, request):
    form = ChangeProfileForm(instance=request.user)
    # form = ProfileFormSet()
    context = dict(form=form)
    return render(request, 'accounts/profile-change.html', context)

  def post(self, request):
    form = ChangeProfileForm(request.POST, request.FILES, instance=request.user)
    if form.is_valid():
      print("form validated")
      form.save()
      # update_session_auth_hash(request=request, user=request.user)
      messages.success(request, 'Profile Updated Successfully')
      return redirect('dashboard')
    context = dict(form=form)
    return render(request, 'accounts/profile-change.html', context) 

@method_decorator(login_required, name='dispatch')
class SetPassword(View):
  def get(self, request):
    form = ChangePasswordForm(user=request.user)
    context = dict(form=form)
    return render(request, 'accounts/change-password.html', context)

  def post(self, request):
    form = ChangePasswordForm(request.user, request.POST)
    if form.is_valid():
      form.save()
      update_session_auth_hash(request=request, user=request.user)
      messages.success(request, 'Password changed successfully')
      return redirect('dashboard')
    context = dict(form=form)
    return render(request, 'accounts/change-password.html', context) 

@method_decorator(login_required, name='dispatch')
class Logout(View):
  def get(self, request):
    logout(request=request)
    return redirect('login')