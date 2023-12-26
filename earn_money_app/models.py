from django.db import models
from home_app.models import UserModel


# Create your models here.
class EarnMoneyModel(models.Model):
    user = models.OneToOneField(UserModel, on_delete=models.CASCADE)
    money_in_day = models.FloatField(default=0)
    money_in_month = models.FloatField(default=0)
    
    def __str__(self) -> str:
        return self.user.username

class SiteRewardTempModel(models.Model):
    endpoint = models.CharField(max_length= 50)
    is_completed = models.BooleanField(default = False)

    def __str__(self):
        return self.endpoint

class GiftCodeModel(models.Model):
    code = models.CharField(default = '', max_length=30, unique =True)
    value = models.FloatField(default= float(0))
    def __str__(self) -> str:
        return self.code


class EarnMoneyWeb1sModel(models.Model):
    user = models.OneToOneField(UserModel, on_delete=models.CASCADE)
    money_of_job = models.FloatField(default=0)
    number_job = models.IntegerField(default=0)
    def __str__(self) -> str:
        return self.user.username
class linkWeb1sStorage(models.Model):
    link = models.CharField(max_length=30)
    list_access_token_user_retrieved = models.JSONField(blank =True) 
    def __str__(self):
        return self.link
    
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