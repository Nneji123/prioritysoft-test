"""
serializers.py file for inventory app.

Author(s): Ifeanyi Nneji
Date: 06/13/2024
"""

from rest_framework import serializers

from .models import Item, Supplier


class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = "__all__"
        extra_kwargs = {"date_added": {"read_only": True}}


class ItemSerializer(serializers.ModelSerializer):
    suppliers = serializers.PrimaryKeyRelatedField(
        queryset=Supplier.objects.all(), many=True, required=False
    )

    class Meta:
        model = Item
        fields = "__all__"
        extra_kwargs = {"date_added": {"read_only": True}}

    def create(self, validated_data):
        suppliers_data = validated_data.pop("suppliers", [])
        item = Item.objects.create(**validated_data)
        item.suppliers.set(suppliers_data)
        return item

    def update(self, instance, validated_data):
        suppliers_data = validated_data.pop("suppliers", None)
        instance = super().update(instance, validated_data)
        if suppliers_data is not None:
            instance.suppliers.set(suppliers_data)
        return instance


class BaseResponseSerializer(serializers.Serializer):
    responseCode = serializers.IntegerField()
    message = serializers.CharField()
    data = serializers.DictField()
