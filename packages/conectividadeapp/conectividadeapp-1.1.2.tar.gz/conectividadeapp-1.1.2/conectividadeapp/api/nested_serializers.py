from conectividadeapp.models import ActivityReason, OldDevice
from rest_framework import serializers
from netbox.api import WritableNestedSerializer
from dcim.models import Device


class NestedDeviceSerializer(WritableNestedSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='dcim-api:device-detail')

    class Meta:
        model = Device
        fields = ['id', 'url', 'name', 'display_name']


class NestedOldDeviceSerializer(WritableNestedSerializer):

    class Meta:
        model = OldDevice
        fields = ['name', 'rack', 'site']


class NestedActivityReasonSerializer(WritableNestedSerializer):

    class Meta:
        model = ActivityReason
        fields = ['name', 'type']
