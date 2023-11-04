from django.urls import path
from . import views


urlpatterns = [
    path('', views.PaySite.as_view(), name='pay')
]
