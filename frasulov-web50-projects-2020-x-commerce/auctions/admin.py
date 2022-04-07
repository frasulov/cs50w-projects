from django.contrib import admin
from .models import *
# Register your models here.


class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name")

class WatchListAdmin(admin.ModelAdmin):
    filter_horizontal = ("item", )
    list_display = ("id", "watcher")

class AuctionAdmin(admin.ModelAdmin):
    list_display = ("id","creator", "category","title", "starting_bid", "created", "is_active")

class BidAdmin(admin.ModelAdmin):
    list_display = ("id", "bid", "bidder", "auction")

class CommentAdmin(admin.ModelAdmin):
    list_display = ("id", "comment_text", "commenter", "auction")

admin.site.register(Auction, AuctionAdmin)
admin.site.register(User)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Bid, BidAdmin)
admin.site.register(WatchList, WatchListAdmin)
admin.site.register(Category, CategoryAdmin)


