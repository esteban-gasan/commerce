from django.contrib import admin

from .models import Category, Item, User


class ItemAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "starting_price", "seller")
    filter_horizontal = ("categories",)


admin.site.register(User)
admin.site.register(Category)
admin.site.register(Item, ItemAdmin)
