from django.db import models
from django.utils import timezone
# Create your models here.


class PostModel(models.Model):
    user = models.CharField(max_length=12)
    title = models.CharField(max_length=255)
    content = models.CharField(max_length=500)
    img = models.ImageField()
    create_at = models.DateTimeField(default=timezone.now, auto_now_add=False)