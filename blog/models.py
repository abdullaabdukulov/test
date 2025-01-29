from django.db import models
from django.urls import reverse
from accounts.models import CustomUser


class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def get_detail_url(self):
        return reverse('blog:post_detail', kwargs={'pk': self.pk})

