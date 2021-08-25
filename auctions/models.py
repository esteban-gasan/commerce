from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Category(models.Model):
    name = models.CharField(max_length=64)

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
