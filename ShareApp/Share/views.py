import os
from django.conf import settings
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from .models import Post, User
from django.views.generic import CreateView, DeleteView, ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q

# Create your views here.
def index(request):
    posts = Post.objects.all()
    context = {
        'posts':posts
    }
    return render(request, 'post/home.html', context)

class PostCreate(LoginRequiredMixin,CreateView):
    model = Post
    template_name = "post/create_post.html"
    fields = ["title", "content", "file"]
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    
class PostListView(ListView):
    model = Post
    template_name = "post/post_list.html"
    context_object_name = 'posts'
    paginate_by = 2


    def get_queryset(self):
        self.user = get_object_or_404(User, username=self.kwargs["username"])
        return Post.objects.filter(user=self.user).order_by("-date_uploaded")
    
class PostDetailView(DetailView):
    model = Post
    template_name = "post/post_detail.html"
    
class PostDelete(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
    model = Post
    template_name = 'post/post_confirm_delete.html'
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.user:
            return True
        return False

from django.views.static import serve

def getfile(request, filename):
    file_path = os.path.join('Files', filename)
    return serve(request, file_path, document_root=settings.MEDIA_ROOT)

def search(request):

    query=request.GET.get('q')

    if query:
        result = Post.objects.filter(
            Q(title__icontains=query) |
            Q(user__username__icontains=query) |
            Q(content__icontains=query)
        )
    else:
        result = Post.objects.none()

    context={ 'posts':result }
    
    return render(request,"post/home.html",context)