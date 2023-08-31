from django.urls import path
from .views import *


urlpatterns = [
    path('',index.as_view(), name='index'),
    path('tracnghiem',Tracnghiem.as_view(), name='tracnghiem'),
    path('',index.as_view, name='index')
]
