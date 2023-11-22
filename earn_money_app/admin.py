from django.contrib import admin
from .models import EarnMoneyFacebookModel, EarnMoneyModel, EarnMoneyTiktokModel, EarnMoneyWeb1sModel, EarnMoneyYoutubeModel

# Register your models here.


admin.site.register(EarnMoneyFacebookModel)
admin.site.register(EarnMoneyModel)
admin.site.register(EarnMoneyTiktokModel)
admin.site.register(EarnMoneyWeb1sModel)
admin.site.register(EarnMoneyYoutubeModel)
