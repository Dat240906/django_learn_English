from django.urls import path
from . import views


urlpatterns = [
    path('', views.EarnMoneySite.as_view(), name='earn_money')
]
