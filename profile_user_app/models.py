from django.db import models
from home_app.models import UserModel
from django.utils import timezone
# Create your models here.
  


class PayByMoMoModel(models.Model):
    user = models.OneToOneField(UserModel, on_delete=models.CASCADE)
    number_account = models.CharField(max_length=20, default='')




class PayByPaypalModel(models.Model):
    user = models.OneToOneField(UserModel, on_delete=models.CASCADE)
    email_account = models.EmailField(max_length=30, default='')
    def __str__(self) -> str:
        return self.user.username


class PayByBankModel(models.Model):
    user = models.OneToOneField(UserModel, on_delete=models.CASCADE)
    name_bank = models.CharField(max_length=20, default='')
    number_account = models.CharField(max_length=20, default='')
    name_account = models.CharField(max_length=30, default='')
    def __str__(self) -> str:
        return self.user.username

class LoginLogModel(models.Model):
    user = models.OneToOneField(UserModel, on_delete=models.CASCADE)
    ip_address = models.CharField(max_length=20)
    browser = models.CharField(max_length=200)
    login_at = models.DateTimeField(default=timezone.now, auto_now_add=False)
    def __str__(self) -> str:
        return self.user.username
    