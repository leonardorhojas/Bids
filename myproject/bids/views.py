from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response

from .models import Bid, Auction
from .serializers import BidSerializer


# Create your views here.

class BidViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list` and `retrieve` actions.
    """
    queryset = Bid.objects.all()
    serializer_class = BidSerializer

    def create(self, request):
        auction_id = request.data.get('auction')
        bid_amount = request.data.get('bid_amount')
        auction = Auction.objects.get(pk=auction_id)

        if auction.end_time < timezone.now():
            return Response(
                {"error": "Auction has already ended."},
                status=status.HTTP_400_BAD_REQUEST
            )

        current_highest_bid = max([bid.bid_amount for bid in auction.bids.all()], default=auction.starting_bid)

        if bid_amount <= current_highest_bid:
            return Response({"error": "Your bid must be higher than the current highest bid."},
                            status=status.HTTP_400_BAD_REQUEST)

        bid = Bid.objects.create(
            auction=auction,
            user=request.user,
            bid_amount=bid_amount
        )

        return Response(BidSerializer(bid).data, status=status.HTTP_201_CREATED)


class AuctionViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list` and `retrieve` actions.
    """
    queryset = Auction.objects.all()
    serializer_class = BidSerializer



