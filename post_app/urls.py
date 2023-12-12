from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    path('', views.index.as_view(), name='index'),
    path('check-cache', views.CheckCache.as_view(), name='check_cache'),
    
    # API
    path('api/v1/create-post/', views.CreatePostApi.as_view(), name='create_post'),
    path('api/v1/add-comment/', views.AddComment.as_view(), name='add_comment'),
    path('api/v1/add-like/', views.AddLike.as_view(), name='add_like'),
]

urlpatterns += static(settings.MEDIA_URL,
                document_root=settings.MEDIA_ROOT)