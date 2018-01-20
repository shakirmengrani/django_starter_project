"""dashboard URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from application import views as app_views
from website import views as web_views
from rest_framework_jwt.views import *

urlpatterns = [
    url(r'^api/access-token/', obtain_jwt_token),
    url(r'^api/refresh-token/', refresh_jwt_token),
    url(r'^api/verify-token/', verify_jwt_token),
    url(r'^admin/', admin.site.urls),
    url(r'^accounts/login/', auth_views.login, name='login'),
    url(r'^accounts/logout/', auth_views.logout, {'template_name': 'registration/logout.html'}, name='logout'),
    url(r'^accounts/profile/', app_views.user_profile, name='profile'),
    url(r'^application/', include("application.urls")),
    url(r'^site/login/', app_views.firebase_user, name='firebase_users'),
    url(r'firebase-messaging-sw.js', web_views.firebase_sw, name='firebase-messaging-sw.js'),
    url(r'^', include("website.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)