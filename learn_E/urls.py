"""
URL configuration for learn_E project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""


from django.contrib import admin
from django.urls import path, include,re_path
from django.conf import settings
from django.conf.urls.static import static

#cấu hình khi DEbug bằng False thì media không hoạt động 
from django.views.static import serve 



urlpatterns = [

    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
    path('24092006/', admin.site.urls),
    # path('/', include('study.urls')),
    path('home/', include('home_app.urls')),
    path('post/', include('post_app.urls')),
    path('setting/', include('setting_app.urls')),
    path('earn_money/', include('earn_money_app.urls')),
    path('pay/', include('pay_app.urls')),
    path('profile_user/', include('profile_user_app.urls')),

]

urlpatterns += static(settings.MEDIA_URL,
                document_root=settings.MEDIA_ROOT)



