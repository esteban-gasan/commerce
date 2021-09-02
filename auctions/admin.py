from django.contrib import admin

from .models import Bid, Category, Comment, Item, User


class UserAdmin(admin.ModelAdmin):
    filter_horizontal = ("watchlist",)


class BidAdmin(admin.ModelAdmin):
    list_display = ("id", "bidder", "bid_amount", "bid_time", "item")


class CommentAdmin(admin.ModelAdmin):
    list_display = ("id", "text", "author", "date_posted", "posted_on")


class ItemAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "active", "starting_price",
                    "seller", "date_listed", "date_closed")
    list_display_links = ("id", "name")
    filter_horizontal = ("categories",)


admin.site.register(User, UserAdmin)
admin.site.register(Bid, BidAdmin)
admin.site.register(Category)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Item, ItemAdmin)
