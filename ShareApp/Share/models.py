import os
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.utils.text import slugify
import uuid
from django.urls import reverse

class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    file = models.FileField(null=True,blank=True, upload_to='Files')
    date_uploaded = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.title
    
    @property
    def extension(self):
        return os.path.splitext(self.file.name)[1].lower()

    def get_absolute_url(self):
        return reverse('post-detail', args = [str(self.id)])
