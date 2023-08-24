from django.db import models
from accounts.models import User


class Category(models.Model):
  name = models.CharField(max_length=155, unique=True)

  def __str__(self) -> str:
    return self.name
  
  def get_published_count(self):
    return self.posts.filter(draft=False).count()
  
  def get_drafted_count(self):
    return self.posts.filter(draft=True).count()
  

class Post(models.Model):
  title = models.CharField(max_length=500)
  image = models.ImageField(upload_to='post-images')
  category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='posts')
  summary = models.TextField()
  content = models.TextField()
  draft = models.BooleanField(verbose_name="Draft", default=False)
  user = models.ForeignKey(User, on_delete=models.CASCADE)

  def __str__(self) -> str:
    return self.title
  
  @staticmethod
  def get_published_count(user=None):
    if user is not None:
      return Post.objects.filter(draft=False, user=user).count()
    else:
      return Post.objects.filter(draft=False).count()
   
  @staticmethod
  def get_draft_count(user=None):
    if user is not None:
      return Post.objects.filter(draft=True, user=user).count()
    else:
      return Post.objects.filter(draft=True).count()


SPECIALITY = (
  ('', 'Select Speciality'),
  ('Dermatologists', 'Dermatologists'),
  ('Pediatrics', 'Pediatrics'),
  ('Orthopedics', 'Orthopedics'),
  ('Cardiologists', 'Cardiologists'),
  ('Neurologist', 'Neurologist'),
  ('Hematologists', 'Hematologists')
)


class Appointment(models.Model):
  speciality = models.CharField(verbose_name="Required Speciality", max_length=100, choices=SPECIALITY)
  start_time = models.DateTimeField(verbose_name="Appointment Date and Time", blank=True, null=True)
  end_time = models.DateTimeField(blank=True, null=True)
  doctor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='doctor')
  patient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='patient') 
  is_attended = models.BooleanField(default=False)
