from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .forms import CategoryForm, PostForm
from .models import Category, Post
from django.contrib import messages
from django.core.paginator import Paginator

limit = 2
post_limit = 5

class Home(View):
  def get(self, request):
    cat_id = request.GET.get('category')
    if cat_id:
      category = get_object_or_404(Category, pk=int(cat_id))
      posts = Post.objects.filter(draft=False, category=category).order_by('-id')
    else:
      posts = Post.objects.filter(draft=False).order_by('-id')
    categories = Category.objects.all()
    published_count = Post.get_published_count()
    paginator = Paginator(posts, per_page=limit)
    page = request.GET.get('page')
    posts = paginator.get_page(page)
    context = dict(posts=posts, categories=categories, published_total_count=published_count)
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

@method_decorator(login_required, name='dispatch')
class PostsShow(View):
  def get(self, request):
    posts = Post.objects.filter(draft=False, user=request.user).order_by("-id")
    drafts = Post.objects.filter(draft=True, user=request.user).order_by("-id")
    categories = Category.objects.filter(posts__user=request.user, posts__draft=False).distinct()
    print(categories)
    published_count = Post.get_published_count(request.user)
    drafted_count = Post.get_draft_count(request.user)
    context = dict(posts=posts, drafts=drafts, categories=categories, published_count=published_count, drafted_count=drafted_count)
    return render(request, 'myapp/publish-posts.html', context)
  
  def post(self, request):
    return render('posts')

@method_decorator(login_required, name='dispatch')
class AllPostShow(View):
  def get(self, request):
    cat_id = request.GET.get('category')
    page = request.GET.get('page')
    if cat_id:
      category = get_object_or_404(Category, pk=cat_id)
      posts = Post.objects.filter(draft=False, category=category).order_by('-id')
      drafts = Post.objects.filter(draft=True, category=category).order_by('-id')
    else:
      posts = Post.objects.filter(draft=False).order_by('-id')
      drafts = Post.objects.filter(draft=True).order_by('-id')
    categories = Category.objects.all()
    published_count = Post.get_published_count()
    drafted_count = Post.get_draft_count()
    paginator = Paginator(posts, per_page=post_limit)
    posts = paginator.get_page(page)
    paginator = Paginator(drafts, per_page=post_limit)
    drafts = paginator.get_page(page)
    context = dict(posts=posts, drafts=drafts, categories=categories, published_count=published_count, drafted_count=drafted_count)
    return render(request, 'myapp/posts.html', context)

@method_decorator(login_required, name='dispatch')
class AddPost(View):
  def get(self, request):
    form = PostForm()
    form1 = CategoryForm()
    categories = Category.objects.all()
    context = dict(form=form, form1=form1, categories=categories)
    return render(request, 'myapp/add-post.html', context)
  
  def post(self, request):
    form = PostForm(request.POST, request.FILES)
    form1 = CategoryForm()
    categories = Category.objects.all()
    if form.is_valid():
      post = form.save(commit=False)
      post.user = request.user
      post.save()
      messages.success(request, 'Post Added Successfully')
      return redirect('posts')
    context = dict(form=form, form1=form1, categories=categories)
    return render(request, 'myapp/add-post.html', context)

@method_decorator(login_required, name='dispatch')
class AddCategory(View):
  def post(self, request):
    form1 = CategoryForm(request.POST)
    categories = Category.objects.all()
    if form1.is_valid():
      form1.save()
      messages.success(request, 'Category Added Successfully')
      return redirect('add-post')
    form = PostForm()
    context = dict(form=form, form1=form1, categories=categories)
    return render(request, 'myapp/add-post.html', context)

@method_decorator(login_required, name='dispatch')
class UpdateCategory(View):
  def post(self, request):
    id = int(request.POST.get('id'))
    name = request.POST.get('category')
    Category(id=id, name=name).save()
    messages.success(request, 'Category Updated Successfully')
    return redirect('add-post')

@method_decorator(login_required, name='dispatch')
class DeleteCategory(View):
  def get(self, request, id):
    Category.objects.filter(id=id).delete()
    messages.success(request, 'Category Deleted Successfully')
    return redirect('add-post')

@method_decorator(login_required, name='dispatch')
class UpdatePost(View):
  def get(self, request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    form = PostForm(instance=post)
    context = dict(form=form)
    return render(request, 'myapp/update-post.html', context)
  
  def post(self, request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    form = PostForm(request.POST, request.FILES, instance=post)
    if form.is_valid():
      post = form.save(commit=False)
      post.user = request.user
      post.save()
      messages.success(request, 'Post Updated Successfully')
      return redirect('posts')
    context = dict(form=form)
    return render(request, 'myapp/update-post.html', context)

@method_decorator(login_required, name='dispatch')
class DeletePost(View):
  def get(self, request, post_id):
    Post.objects.filter(id=post_id).delete()
    return redirect('posts')

  def post(self, request):
    pass

@method_decorator(login_required, name='dispatch')
class PostDetail(View):
  def get(self, request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    context = dict(post=post)
    return render(request, 'myapp/post-detail.html', context)

class Search(View):
  def get(self, request):
    cat_id = request.GET.get('category')
    query = request.GET.get('query').strip()
    if cat_id:
      category = get_object_or_404(Category, pk=int(cat_id))
      posts = Post.objects.filter(draft=False, category=category, title__icontains=query).order_by('-id')
    else:
      posts = Post.objects.filter(draft=False, title__icontains=query).order_by('-id')
    categories = Category.objects.all()
    published_count = Post.get_published_count()
    paginator = Paginator(posts, per_page=limit)
    page = request.GET.get('page')
    posts = paginator.get_page(page)
    total_result = paginator.count
    context = dict(posts=posts, categories=categories, published_total_count=published_count, query=query, total_result=total_result)
    return render(request, 'myapp/search.html', context)
