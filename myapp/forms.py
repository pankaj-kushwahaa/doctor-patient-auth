from re import A
from django import forms
from .models import Category, Post


class CategoryForm(forms.ModelForm):
  class Meta:
    model = Category
    fields = ['name']
    widgets = {
      'name' : forms.TextInput(attrs={'class':'form-control'})
    }
    error_messages = {
      'name': {'required':'Category is required'}
    }

class PostForm(forms.ModelForm):
  class Meta:
    model = Post
    fields = '__all__'
    exclude = ('user',)
    widgets = {
      'title': forms.TextInput(attrs={'class':'form-control', 'autofocus':''}),
      'image': forms.FileInput(attrs={'class':'form-control'}),
      'category': forms.Select(attrs={'class':'form-control'}),
      'summary': forms.Textarea(attrs={'class':'form-control', 'rows':'3'}),
      'content': forms.Textarea(attrs={'class':'form-control', 'rows':'5'}),
      'draft': forms.CheckboxInput(attrs={'class':'form-check-input', 'style':'cursor:pointer;'})
    }
    
