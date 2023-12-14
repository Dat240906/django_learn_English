from django.urls import path
from . import views


urlpatterns = [
    path('', views.SettingSite.as_view(), name='setting'),
    path('api/v1/change-password/', views.ChangePasswordAPI.as_view(), name='change_pass')
]
