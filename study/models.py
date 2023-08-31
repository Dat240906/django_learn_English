from django.db import models

# Create your models here.





class QuestionsModel(models.Model):
    question = models.CharField(max_length=255)


    def __str__(self) -> str:
        return self.question


class AnswersModel(models.Model):
    question = models.ForeignKey(QuestionsModel, on_delete=models.CASCADE, related_name='answer')
    answer = models.CharField(max_length=255)


    def __str__(self) -> str:
        return self.answer