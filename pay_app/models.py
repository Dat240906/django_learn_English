from django.db import models
from home_app.models import UserModel
# Create your models here.


#tiền khả dụng 
class MoneyCanWithdraw(models.Model):
    user = models.OneToOneField(UserModel, on_delete=models.CASCADE)
    money = models.FloatField(default=0)
    
    def __str__(self) -> str:
        return self.user.username




#tiền khi tuyển ref
class MoneyRef(models.Model):
    user = models.OneToOneField(UserModel, on_delete=models.CASCADE)
    money = models.FloatField(default=0)
    
    def __str__(self) -> str:
        return self.user.username



#tiền đang chờ rút
class MoneyWaitWithdraw(models.Model):
    user = models.OneToOneField(UserModel, on_delete=models.CASCADE)
    money = models.FloatField(default=0)
    
    def __str__(self) -> str:
        return self.user.username
    


#tiền bị thu hồi
class MoneyRevoked(models.Model):
    user = models.OneToOneField(UserModel, on_delete=models.CASCADE)
    money = models.FloatField(default=0)
    
    def __str__(self) -> str:
        return self.user.username
    


#tiền đã phê duyệt (đã rút)
class MoneyValidated(models.Model):
    user = models.OneToOneField(UserModel, on_delete=models.CASCADE)
    money = models.FloatField(default=0)
    
    def __str__(self) -> str:
        return self.user.username
    


#tổng só tiền rút (bao gồn cả tiền bị thu hồi)
class MoneyTotal(models.Model):
    user = models.OneToOneField(UserModel, on_delete=models.CASCADE)
    money = models.FloatField(default=0)
    
    def __str__(self) -> str:
        return self.user.username
 