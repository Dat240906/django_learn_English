from django.urls import path
from . import views





urlpatterns = [
    path('login/', views.Login.as_view(), name='login'),    
    path('register/', views.Register.as_view(), name='register'),    
    path('', views.Home.as_view(), name='home'),
    path('showcache/', views.ShowCache.as_view(), name='showcache'),

    ########## API ###########
    path('api/v1/post-comments/', views.APIGetPostComment().as_view(), name='getpost')
]


