import time
from datetime import datetime

from django.contrib.auth.models import User
from django.db import models, transaction


class Auction(models.Model):
    title = models.CharField(max_length=40)
    description = models.TextField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    start_bid = models.FloatField()
    winning_bid = models.ForeignKey('Bid', on_delete=models.CASCADE, related_name='winning_bid')

    def __str__(self):
        return self.title

    @property
    def completed(self):
        if datetime.now() >= self.end_date:
            return True
        if self.winning_bid is not None:
            return True
        return False

    @transaction.atomic()
    def assign_bid(self, bid_data):
        if not self.completed:
            wining_bid = self.bids.order_by('-bid').first()
            if wining_bid:
                self.winning_bid = wining_bid
                self.save()


class Bid(models.Model):
    bid = models.FloatField()
    bidder = models.ForeignKey(User, on_delete=models.CASCADE)
    auction = models.ForeignKey(Auction, related_name='bids', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.bidder}'s bid is {self.bid} for auction {self.auction}"

