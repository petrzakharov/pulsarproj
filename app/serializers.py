from rest_framework import serializers
from app.models import Item
from .fields import ImageField


class ItemSerializer(serializers.ModelSerializer):
    image = ImageField()

    class Meta:
        model = Item
        fields = ('title', 'part_number', 'price', 'status', 'image',)
