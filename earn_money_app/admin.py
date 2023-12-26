from django.contrib import admin
from .models import EarnMoneyFacebookModel,linkWeb1sStorage,SiteRewardTempModel,GiftCodeModel, EarnMoneyModel,EarnMoneyWeb1sModel ,EarnMoneyTiktokModel, EarnMoneyYoutubeModel

# Register your models here.


admin.site.register(EarnMoneyFacebookModel)
admin.site.register(EarnMoneyModel)
admin.site.register(EarnMoneyWeb1sModel)
admin.site.register(EarnMoneyTiktokModel)
admin.site.register(EarnMoneyYoutubeModel)
admin.site.register(GiftCodeModel)
admin.site.register(SiteRewardTempModel)
admin.site.register(linkWeb1sStorage)
