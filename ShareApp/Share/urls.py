from django.urls import path
from .views import (PostCreate, PostDetailView,PostListView,PostDelete)
from . import views
urlpatterns = [
    path('', views.index, name='home'),
    path('create_post/', PostCreate.as_view(), name='post'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('user/posts/<username>', PostListView.as_view(), name='post-list'),
    path('post/<int:pk>/delete', PostDelete.as_view(), name='post-delete'),
    path('post/search/', views.search, name='search'),


]
