from django.contrib.auth.models import User, Group
from .models import *
from rest_framework import viewsets
from .serializers import *

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = category.objects.filter(activeyn=1)
    serializer_class = CategorySerializer

class ArtistViewSet(viewsets.ModelViewSet):
    queryset = artist.objects.filter(activeyn=1)
    serializer_class = ArtistSerializer