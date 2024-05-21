
from django.urls import path, include
from .views import BidViewSet, AuctionViewSet


urlpatterns = [
    path('bids/', BidViewSet.as_view({'get': 'list', 'post': 'create', 'put': 'update', 'delete': 'destroy'})),
    path('auctions/', AuctionViewSet.as_view({'get': 'list', 'post': 'create', 'put': 'update', 'delete': 'destroy'})),
]