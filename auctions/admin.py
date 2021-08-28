from django.contrib import admin

from .models import Category, Item, User
class UserAdmin(admin.ModelAdmin):
    filter_horizontal = ("watchlist",)

class ItemAdmin(admin.ModelAdmin):
    list_display = ("id", "active", "name", "starting_price",
                    "seller", "date_listed", "date_closed")
    filter_horizontal = ("categories",)


admin.site.register(User, UserAdmin)
admin.site.register(Category)
admin.site.register(Item, ItemAdmin)
