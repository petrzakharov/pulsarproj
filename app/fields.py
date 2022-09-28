from rest_framework import fields

from app.models import Item


class ImageField(fields.ImageField):
    def to_representation(self, value):
        path, extension = value.url.split('.')
        formats = [
            extension.upper(),
        ]
        if extension.upper() in Item.FROM_REENCODE:
            formats.append('WEBP')

        return {
            'path': path,
            'formats': formats
        }
