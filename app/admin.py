from django.contrib import admin

from .models import Item

admin.site.register(Item)


class MyAdmin(admin.ModelAdmin):
    pass
