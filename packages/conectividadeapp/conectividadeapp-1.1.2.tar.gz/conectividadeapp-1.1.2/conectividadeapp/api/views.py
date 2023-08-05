from conectividadeapp.models import Actor, ActorCategory, Activity
from . import serializers
from rest_framework.viewsets import ModelViewSet
from rest_framework.routers import APIRootView


class ConectividadeappRootView(APIRootView):
    """ ConectividadeApp Root View """
    def get_view_name(self):
        return 'ConectividadeApp'


class ActorViewSet(ModelViewSet):
    queryset = Actor.objects.all()
    serializer_class = serializers.ActorSerializer
    name = 'actor-list'


class ActorCategoryViewSet(ModelViewSet):
    queryset = ActorCategory.objects.all()
    serializer_class = serializers.ActorCategorySerializer
    name = 'actorcategory-list'


class ActivityViewSet(ModelViewSet):
    queryset = Activity.objects.all()
    serializer_class = serializers.ActivitySerializer
    name = 'activity-list'
