from django.contrib import admin
from .models import RankModel, RankingModel, NotificationUserModel, UserModel, NotificationCommomModel


# Register your models here.

admin.site.register(UserModel)
admin.site.register(RankingModel)
admin.site.register(RankModel)
admin.site.register(NotificationUserModel)
admin.site.register(NotificationCommomModel)