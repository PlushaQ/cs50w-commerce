from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.text import slugify

import uuid, datetime
from decimal import Decimal


class User(AbstractUser):
    pass

class Category(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField(max_length=500)
    
    def __str__(self) -> str:
        return self.title

class Auction(models.Model):
    title = models.CharField(max_length=75)
    description = models.TextField(max_length=5000)
    slug = models.SlugField(max_length=255, blank=True)
    image = models.URLField()
    release_date = models.DateTimeField(blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    start_value = models.DecimalField(max_digits=8, decimal_places=2)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='auctions_created')

    active = models.BooleanField(default=True)
    winner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, default=None, related_name='auctions_winner')

    def __str__(self):
        return self.title
    
    def short_description(self):
        return self.description[:255] + '...' if len(self.description) > 255 else self.description

    def pretty_release_date(self):
        return self.release_date.strftime("%e %b %Y")
    
    def close_auction(self, winner):
        self.active = False
        self.winner = winner


    def save(self, *args, **kwargs):
        self.release_date = datetime.datetime.now()
        self.slug = slugify(self.title + '-' + str(uuid.uuid4())[:8])
        self.start_value = self.start_value * 100
        super(Auction, self).save(*args, **kwargs)

class Bid(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE)
    bid_date = models.DateTimeField(auto_now_add=True)
    value = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self) -> str:
        return f'Bid {self.value} on {self.auction} by {self.user} on {self.bid_date}'

    @classmethod
    def biggest_bid(cls, auction):
        biggest_bid = cls.objects.filter(auction=auction).aggregate(models.Max('value'))['value__max']
        if biggest_bid is None:
            return auction.start_value
        return biggest_bid
    
    @classmethod
    def winner_bid(cls, auction):
        try:
            winner_bid = cls.objects.filter(auction=auction).latest('value')
            return winner_bid
        except cls.DoesNotExist:
            return None
    
    @classmethod
    def number_of_bids(cls, auction):
        number = len(cls.objects.filter(auction=auction))
        return number
    
    def save(self, *args, **kwargs):
        current_highest_bid = Bid.biggest_bid(self.auction)
        if self.value < current_highest_bid:
            return False
        
        super(Bid, self).save(*args, **kwargs)


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(max_length=5000)

class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='watchlist')
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f'Auction {self.auction} published by {self.auction.user}.'