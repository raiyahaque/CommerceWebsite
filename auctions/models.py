from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Listing(models.Model):
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=200)
    starting_bid = models.IntegerField()
    image_url = models.URLField(null=True, max_length=300)
    category = models.CharField(null=True, max_length=64)
    users = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings")
    current_price = models.IntegerField()
    active = models.BooleanField(default=True)
    winner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listing_winner", null=True)
    creation_time = models.DateTimeField(auto_now=True)

class Bid(models.Model):
    bid_amount = models.IntegerField()
    users = models.ForeignKey(User, on_delete=models.CASCADE, related_name="biddings")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bids")

class Watchlist(models.Model):
    users = models.ForeignKey(User, on_delete=models.CASCADE, related_name="watchlistings")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="watchlisted")

class Commentary(models.Model):
    comment = models.CharField(max_length=300)
    users = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comment")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="listing_comment")
