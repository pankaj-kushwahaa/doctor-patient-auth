from django.urls import path
from . import views

urlpatterns = [
  path('', views.Home.as_view(), name='home'),
  path('dashboard/', views.Dashboard.as_view(), name='dashboard'),
  path('add-post/', views.AddPost.as_view(), name='add-post'),
  path('add-category/', views.AddCategory.as_view(), name='add-category'),
  path('update-post/<int:post_id>/', views.UpdatePost.as_view(), name='update-post'),
  path('delete-post/<int:post_id>/', views.DeletePost.as_view(), name='delete-post'),
  path('posts/', views.PostsShow.as_view(), name='posts'),
  path('delete-category/<int:id>/', views.DeleteCategory.as_view(), name='delete-category'),
  path('update-category/', views.UpdateCategory.as_view(), name='update-category'),
  path('post-detail/<int:post_id>/', views.PostDetail.as_view(), name='post-detail'),
  path('all-posts/', views.AllPostShow.as_view(), name='all-posts'),
  path('search/', views.Search.as_view(), name='search'),
]