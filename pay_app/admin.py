from django.contrib import admin
from .models import MoneyCanWithdraw, MoneyRef, MoneyRevoked, MoneyTotal, MoneyValidated, MoneyWaitWithdraw
# Register your models here.


admin.site.register(MoneyCanWithdraw)
admin.site.register(MoneyRef)
admin.site.register(MoneyRevoked)
admin.site.register(MoneyTotal)
admin.site.register(MoneyValidated)
admin.site.register(MoneyWaitWithdraw)
