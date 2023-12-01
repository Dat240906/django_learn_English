from collections.abc import Iterable
from django.db import models
from django.utils import timezone
import home_app
from home_app.models import UserModel, generate_random_string
# Create your models here.


class PostModel(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    content = models.CharField(max_length=500, blank=True)
    img = models.ImageField(blank=True, null=True)
    create_at = models.DateTimeField(default=timezone.now, auto_now_add=False)
    num_like = models.IntegerField(default=0)
    num_comment = models.IntegerField(default=0)
    num_share =  models.IntegerField(default=0)
    post_id = models.CharField(max_length=50, default='', blank=True)

    def save(self, *args, **kwargs):
        
        if not self.post_id:
            self.post_id = f'{generate_random_string()}'
        super().save(*args, **kwargs)
    def __str__(self) -> str:
        return f'{self.user.username} - {self.title}'
class CommentModel(models.Model):
    post = models.ForeignKey(PostModel, on_delete=models.CASCADE)
    user = models.CharField(max_length=12)
    content_comment = models.CharField(max_length=200)
    create_at = models.DateTimeField(default=timezone.now, auto_now_add=False)
    def __str__(self) -> str:
        return f'{self.post.title} - {self.user}'