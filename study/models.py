from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.




class StorageDataModel(models.Model):
    name_data = models.CharField(max_length=40)
    data = models.CharField(max_length=5000) #dữ liệu dưới dạng str anh:viet, anh:viet
    
    def __str__(self) -> str:
        return self.name_data

class NotificationsModel(models.Model):
    message = models.CharField(max_length=1500)

class UserModel(models.Model):
    ip_address = models.GenericIPAddressField()
    username = models.CharField(max_length=12, unique=True)
    password = models.CharField(max_length=12)
    count_pass = models.IntegerField(default=0)
    money = models.CharField(default=0, max_length=20)
    is_seen_noti = models.BooleanField(default=True)
    message = models.CharField(max_length=1500, null=True)
    

    def __str__(self):
        return self.username
    




class ContactModel(models.Model):
    user = models.CharField(max_length=12, null=True)
    message = models.CharField(max_length=255)
    def __str__(self) -> str:
        return self.massage

class WithdrawMoneyModel(models.Model):
    gmail = models.EmailField(null=True)
    username = models.CharField(max_length=12, null=True)
    money = models.CharField(default=0, max_length=30)
    stk = models.CharField(max_length=20)
    ttk = models.CharField(max_length=50)
    bank = models.CharField(max_length=20)
    def __str__(self) -> str:
        return self.money

class QuestionsModel(models.Model):
    
    question = models.CharField(max_length=255)


    def __str__(self) -> str:
        return self.question


class AnswersModel(models.Model):
    question = models.ForeignKey(QuestionsModel, on_delete=models.CASCADE, related_name='answer')
    answer = models.CharField(max_length=255)


    def __str__(self) -> str:
        return self.answer