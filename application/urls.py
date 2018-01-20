from django.conf.urls import url, include
from rest_framework import routers
from . import views, api_views, serializers


router = routers.DefaultRouter()
router.register(r'users', api_views.UserViewSet)
router.register(r'groups', api_views.GroupViewSet)
router.register(r'category', serializers.CategoryViewSet)
router.register(r'artist', api_views.ArtistViewSet)


urlpatterns = [
    url(r'^rest-api/', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^album/', views.album_page, name="album"),
    url(r'^album_search/', views.album_search_page, name="albumSearch"),
    url(r'^track/', views.track_page, name="track"),
    url(r'^video/', views.video_page, name="video"),
    url(r'^carousel/', views.carousel_page, name="carousel"),
    url(r'^category/', views.category_page, name="category"),
    url(r'^artist/', views.artist_page, name="artist"),
    url(r'$', views.welcome, name="welcome"),
]
