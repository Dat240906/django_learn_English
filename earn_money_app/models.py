from django.db import models
from home_app.models import UserModel


# Create your models here.
class EarnMoneyModel(models.Model):
    user = models.OneToOneField(UserModel, on_delete=models.CASCADE)
    money_in_day = models.FloatField(default=0)
    money_in_month = models.FloatField(default=0)
    
    def __str__(self) -> str:
        return self.user.username


class EarnMoneyWeb1sModel(models.Model):
    user = models.OneToOneField(UserModel, on_delete=models.CASCADE)
    money_of_job = models.FloatField(default=0)
    number_job = models.IntegerField(default=0)
    def __str__(self) -> str:
        return self.user.username
    

class EarnMoneyFacebookModel(models.Model):
    user = models.OneToOneField(UserModel, on_delete=models.CASCADE)
    money_of_job = models.FloatField(default=0)
    number_job = models.IntegerField(default=0)
    def __str__(self) -> str:
        return self.user.username
    

class EarnMoneyTiktokModel(models.Model):
    user = models.OneToOneField(UserModel, on_delete=models.CASCADE)
    money_of_job = models.FloatField(default=0)
    number_job = models.IntegerField(default=0)
    def __str__(self) -> str:
        return self.user.username
    

class EarnMoneyYoutubeModel(models.Model):
    user = models.OneToOneField(UserModel, on_delete=models.CASCADE)
    money_of_job = models.FloatField(default=0)
    number_job = models.IntegerField(default=0)
    def __str__(self) -> str:
        return self.user.username