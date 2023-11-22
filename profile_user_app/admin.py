from django.contrib import admin
from .models import LoginLogModel, PayByMoMoModel, PayByBankModel, PayByPaypalModel


# Register your models here.



admin.site.register(LoginLogModel)
admin.site.register(PayByMoMoModel)
admin.site.register(PayByBankModel)
admin.site.register(PayByPaypalModel)
