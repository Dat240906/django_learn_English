from django.urls import path
from . import views


urlpatterns = [
    path('', views.ProfileSite.as_view(), name='profile')
]
