from django.urls import path
from . import views


urlpatterns = [
    path('', views.EarnMoneySite.as_view(), name='earn_money'),
    path('reward/<str:endpoint>/',views.HandleRewardSiteTemp.as_view(), name='reward_site_temp'),
    path('plus-money/', views.HandlePlusMoneyByAccessToken.as_view(), name = 'plus_money'),
    path('create-giftcode/', views.CreateGiftcode.as_view(), name='create_giftcode'),
    path('delete-endpoint/', views.DeleteRewardSiteTemp.as_view(), name='delete_endpoint'),
    path('get-money/', views.EarnMoneyGetCoin.as_view(), name='get_money'),
    path('get-job-web1s/', views.getJobWeb1sAPI.as_view(), name='get_job_web1s'),
    path('create-link-web1s/', views.CreatelinkWeb1s.as_view(), name='create_link_web1s'),


    path('youtube/', views.EarnMoneyYoutube.as_view(), name='youtube'),
    path('web1s/', views.EarnMoneyWeb1s.as_view(), name='web_1s'),
    path('tiktok/', views.EarnMoneyTiktok.as_view(), name='tiktok'),
    path('facebook/', views.EarnMoneyFacebook.as_view(), name='facebook'),
]
