from django.db import models

# Create your models here.



class UserModel(models.Model):
    ip_address = models.GenericIPAddressField()
    username = models.CharField(max_length=25,unique=True)
    count_pass = models.IntegerField(default=0)
    def __str__(self) -> str:
        return self.username

class StorageDataModel(models.Model):
    name_data = models.CharField(max_length=40)
    data = models.CharField(max_length=5000) #dữ liệu dưới dạng str anh:viet, anh:viet
    
    
    def __str__(self) -> str:
        return self.name_data

class QuestionsModel(models.Model):
    
    question = models.CharField(max_length=255)


    def __str__(self) -> str:
        return self.question


class AnswersModel(models.Model):
    question = models.ForeignKey(QuestionsModel, on_delete=models.CASCADE, related_name='answer')
    answer = models.CharField(max_length=255)


    def __str__(self) -> str:
        return self.answer