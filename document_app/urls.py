from django.urls import path
from . import views


urlpatterns = [
    path('', views.DocumentSite.as_view(), name='document')
]
