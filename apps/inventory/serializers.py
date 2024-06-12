from rest_framework import serializers

from .models import Item, Supplier


class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = "__all__"
        extra_kwargs = {
            'date_added': {'read_only': True}
        }


class ItemSerializer(serializers.ModelSerializer):
    suppliers = SupplierSerializer(many=True, read_only=True)

    class Meta:
        model = Item
        fields = "__all__"
        extra_kwargs = {
            'date_added': {'read_only': True}
        }


class BaseResponseSerializer(serializers.Serializer):
    responseCode = serializers.IntegerField()
    message = serializers.CharField()
    data = serializers.DictField()
