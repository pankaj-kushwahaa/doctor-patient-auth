from django.contrib import admin
from .models import Post, Category, Appointment

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
  list_display = ['name', 'id']

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
  list_display = ['title', 'category', 'image', 'draft', 'user', 'id']
  list_filter = ['draft', 'category']

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
  list_display = ['speciality', 'start_time', 'doctor', 'patient']