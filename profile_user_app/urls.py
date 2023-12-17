from django.urls import path
from . import views


urlpatterns = [
    path('', views.ProfileSite.as_view(), name='profile_user'),
    path('api/v1/update-data/', views.UpdateDataUserAPI.as_view(), name='update_data'),
    path('api/v1/add-bank/', views.AddMethodAPI.as_view(), name='add_bank'),
    path('api/v1/get-post/', views.GetPostsAPI.as_view(), name='get_posts')
]
