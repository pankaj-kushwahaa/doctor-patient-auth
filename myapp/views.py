from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from accounts.models import User

class Home(View):
  def get(self, request):
    doctors = User.objects.filter(user_type='Doctor')
    patients = User.objects.filter(user_type='Patient')
    context = dict(doctors=doctors, patients=patients)
    return render(request, 'myapp/home.html', context)

@method_decorator(login_required, name='dispatch')
class Dashboard(View):
  def get(self, request):
    if request.user.user_type == 'Doctor':
     return render(request, 'myapp/doctor-dashboard.html')
    else:
      return render(request, 'myapp/patient-dashboard.html')

  def post(self, request):
    return redirect('home')
