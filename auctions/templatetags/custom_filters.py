from django import template
from auctions.models import Bid, Auction
from django.shortcuts import get_object_or_404

register = template.Library()

@register.filter
def get_biggest_bid(auction):
    biggest_bid = Bid.biggest_bid(auction)
    formatted_bid = "{:.2f}".format(biggest_bid)
    return formatted_bid


@register.filter
def get_number_of_bids(auction):
    return Bid.number_of_bids(auction)


@register.filter
def get_auction_slug(auction):
    return auction.slug