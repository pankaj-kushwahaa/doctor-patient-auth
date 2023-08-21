from django.contrib import admin
from .models import Post, Category

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
  list_display = ['name', 'id']

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
  list_display = ['title', 'category', 'image', 'draft', 'user', 'id']
  list_filter = ['draft', 'category']
