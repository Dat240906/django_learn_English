from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    path('', views.index.as_view(), name='index'),

    # API
    path('api/v1/create-post/', views.CreatePostApi.as_view(), name='create_post')
]

urlpatterns += static(settings.MEDIA_URL,
                document_root=settings.MEDIA_ROOT)