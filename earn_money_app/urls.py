from django.urls import path
from . import views


urlpatterns = [
    path('', views.EarnMoneySite.as_view(), name='earn_money'),
    path('link1s/', views.EarnMoneyLink1s.as_view(), name='link1s'),
    path('web1s/', views.EarnMoneyWeb1s.as_view(), name='web1s'),
    path('youtube/', views.EarnMoneyYoutube.as_view(), name='youtube'),
    path('tiktok/', views.EarnMoneyTiktok.as_view(), name='tiktok'),
    path('facebook/', views.EarnMoneyFacebook.as_view(), name='facebook'),
]
