from django.contrib import admin
from .models import User, Listing, Bid, Watchlist, Commentary

# Register your models here.
admin.site.register(User)

@admin.register(Listing)
class ListingAdmin(admin.ModelAdmin):
    list_display = ['title', 'starting_bid', 'category', 'users', 'current_price', 'active']

@admin.register(Bid)
class BidAdmin(admin.ModelAdmin):
    list_display = ['bid_amount', 'users', 'listing']

admin.site.register(Watchlist)
admin.site.register(Commentary)
