from collections.abc import Iterable
from django.db import models
from django.utils import timezone
import secrets
import string


#random chuỗi ngẫu nhiên
def generate_random_string(length=20):
    characters = string.ascii_letters + string.digits
    random_string = ''.join(secrets.choice(characters) for _ in range(length))
    return random_string


class UserModel(models.Model):
    username = models.CharField(max_length=12, unique=True)
    password = models.CharField(max_length=20)
    money = models.FloatField(default=0)
    email = models.EmailField(default='', max_length=50, blank=True)
    number_phone = models.CharField(default='', max_length=20, blank=True)
    address = models.CharField(default='',max_length=50, blank=True)
    avatar = models.ImageField( default="base-user.png", null=True)
    access_token = models.CharField(default='', max_length=50, blank=True)
    ip_address = models.CharField(default='', max_length=50, blank=True)
    def save(self,*args, **kwargs) :
        if not self.access_token:
            self.access_token = f'test_{generate_random_string()}'
        super().save(*args, **kwargs)
    def __str__(self) -> str:
        return self.username




class RankModel(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    def __str__(self) -> str:
        return self.user.username



class NotificationCommomModel(models.Model):
    content = models.CharField(max_length=1080)
    create_at = models.DateTimeField(default=timezone.now,  auto_now_add=False)
    def __str__(self):
        return self.content
    



class NotificationUserModel(models.Model):
    user = models.OneToOneField(UserModel, on_delete=models.CASCADE)
    content = models.CharField(max_length=1080)
    create_at = models.DateTimeField(default=timezone.now,  auto_now_add=False)
    def __str__(self):
        return self.user.username
    



class RankingModel(models.Model):
    user = models.OneToOneField(UserModel, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.user.username