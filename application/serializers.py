from django.contrib.auth.models import User, Group
from rest_framework import serializers, viewsets
from .models import category, artist


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'groups')


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')

class CategorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = category
        fields = ('id', 'name', 'feature', 'type')

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = category.objects.filter(activeyn=1)
    serializer_class = CategorySerializer

class ArtistSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = artist
        fields = ('id', 'name', 'activeyn')