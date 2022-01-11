from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.base import ModelState
from django.db.models.deletion import CASCADE


class User(AbstractUser):
    pass


class Auctions(models.Model):
    name = models.CharField(max_length = 40)
    description = models.CharField(max_length=40)
    image_url = models.URLField(default="", blank=True)
    category = models.CharField(max_length=40, default="", blank=True)
    user_created_auction = models.ForeignKey(User, on_delete=CASCADE, default=None)
    is_active = models.BooleanField(default=True)

    def __str__(self) -> str:
        return f"{self.name}, {self.description}, {self.category} from {self.user_created_auction}"


class Bids(models.Model):
    starting_bid = models.IntegerField()
    last_bid = models.IntegerField(default=0)
    auction = models.OneToOneField(Auctions, on_delete=CASCADE, default=None , related_name="bids_auction")
    user_who_made_last_successful_bid = models.ForeignKey(User, on_delete=CASCADE, default=None, null=True)

    def __str__(self) -> str:
        return f"Staring bid is{self.starting_bid}, the last_bid is {self.last_bid} for {self.auction}"


class Commet(models.Model):
    commet = models.CharField(max_length=360)
    user = models.ForeignKey(User, on_delete=CASCADE, null=True )
    auction = models.ForeignKey(Auctions, on_delete=CASCADE, null=True)

    def __str__(self) -> str:
        return f"{self.commet} from {self.user} for {self.auction}"

class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=CASCADE, related_name="user_watchlist")
    auction = models.ForeignKey(Auctions, on_delete=CASCADE, related_name="user")

    def __str__(self) -> str:
        return f"user {self.user} adds {self.auction}"


