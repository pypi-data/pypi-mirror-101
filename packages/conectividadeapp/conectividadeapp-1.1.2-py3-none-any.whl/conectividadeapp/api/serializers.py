from .nested_serializers import NestedActivityReasonSerializer, NestedDeviceSerializer, NestedOldDeviceSerializer
from rest_framework import serializers
from conectividadeapp import models


class ActorSerializer(serializers.ModelSerializer):

    category = serializers.SlugRelatedField(
        queryset=models.ActorCategory.objects.all(),
        slug_field='name'
    )

    class Meta:
        model = models.Actor
        fields = (
            '__all__'
        )


class ActorCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ActorCategory
        fields = (
            '__all__'
        )


class ActivitySerializer(serializers.ModelSerializer):
    device = NestedDeviceSerializer(read_only=True)
    actor = serializers.SlugRelatedField(
        queryset=models.Actor.objects.all(),
        slug_field='name',
        many=True
    )
    reason = NestedActivityReasonSerializer(read_only=True)
    olddevice = NestedOldDeviceSerializer(read_only=True)

    class Meta:
        model = models.Activity
        fields = (
            '__all__'
        )
