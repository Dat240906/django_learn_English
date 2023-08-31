from django.urls import path
from .views import index, Tracnghiem, Tuluan, reset, reset_TN, reset_TL



urlpatterns = [
    path('', index.as_view(), name='index'),
    path('tracnghiem/', Tracnghiem.as_view(), name='tracnghiem'),
    path('tuluan/', Tuluan.as_view(), name='tuluan'),
    path('reset/', reset, name='reset'),
    path('reset_TN/', reset_TN, name='reset_TN'),
    path('reset_TL/', reset_TL, name='reset_TL'),
]
