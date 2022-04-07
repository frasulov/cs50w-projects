from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import datetime

# author: Fagan Rasulov
# github: frasulov


class User(AbstractUser):
    pass


class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.name}"


class Auction(models.Model):
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=64)
    img_url = models.CharField(blank=True, max_length=255, default="https://us.123rf.com/450wm/pavelstasevich/pavelstasevich1811/pavelstasevich181101028/112815904-stock-vector-no-image-available-icon-flat-vector-illustration.jpg?ver=6")
    category = models.ForeignKey(Category, blank=True, on_delete=models.CASCADE, related_name="auctions")
    is_active = models.BooleanField(default=True)
    starting_bid = models.DecimalField(max_digits=15, decimal_places=2)
    created = models.CharField(max_length=64, default= datetime.now().strftime("%B %d, %Y %H:%M:%S"))
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="auctions")

    def __str__(self):
        return f"Item: {self.title} creator: {self.creator} created: {self.created}"


class WatchList(models.Model):
    watcher = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings")
    item = models.ManyToManyField(Auction, blank=True, null=True, related_name="wather_list")


    def __str__(self):
        return f"Watcher: {self.watcher} {self.item}"

class Comment(models.Model):
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name="comments")
    comment_text = models.CharField(max_length=255)
    commenter = models.ForeignKey(User, on_delete=models.CASCADE, related_name="my_comments")

    def __str__(self):
        return f"Commenter: {self.commenter} Comment: {self.comment_text}"

class Bid(models.Model):
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name="bids")
    bid = models.DecimalField(max_digits=15, decimal_places=2)
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name="my_bids")

    def __str__(self):
        return f"{self.auction} 'bids "

