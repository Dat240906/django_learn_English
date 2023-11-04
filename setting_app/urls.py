from django.urls import path
from . import views


urlpatterns = [
    path('', views.SettingSite.as_view(), name='setting')
]
