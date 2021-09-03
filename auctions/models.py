from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    watchlist = models.ManyToManyField(
        "Item", blank=True, related_name="saved_by")


class Category(models.Model):
    name = models.CharField(max_length=64, unique=True)

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "categories"

    def __str__(self) -> str:
        return self.name


class Item(models.Model):
    name = models.CharField(max_length=256)
    description = models.TextField()
    starting_price = models.DecimalField(max_digits=10, decimal_places=2)
    image_url = models.URLField(max_length=256, blank=True)
    seller = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="items_for_sale")
    categories = models.ManyToManyField(
        Category, blank=True, related_name="items")
    date_listed = models.DateTimeField(auto_now_add=True)
    date_closed = models.DateTimeField(blank=True, null=True)
    winner = models.ForeignKey(
        User, on_delete=models.SET_NULL, blank=True, null=True, related_name="won_items")
    winning_bid_amount = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ["-date_listed"]

    def __str__(self) -> str:
        return f"{self.id}: {self.name}"


class Bid(models.Model):
    item = models.ForeignKey(
        Item, on_delete=models.CASCADE, related_name="bids")
    bidder = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user_bids")
    bid_amount = models.DecimalField(max_digits=10, decimal_places=2)
    bid_time = models.DateTimeField(auto_now_add=True)


class Comment(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.SET_DEFAULT, default="User", related_name="user_comments")
    posted_on = models.ForeignKey(
        Item, on_delete=models.CASCADE, related_name="comments")
    text = models.TextField()
    date_posted = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-date_posted"]
