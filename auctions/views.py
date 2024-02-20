from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages


from datetime import datetime

from .models import Comment, User, Auction, Bid, Watchlist, Category
from .forms import AuctionForm, BidForm, CommentForm


def index(request):
    auctions = Auction.objects.all()
    biggest_bids = {}
    for auction in auctions:
        biggest_bids[auction] = Bid.biggest_bid(auction)
    return render(request, "auctions/index.html", {'auctions': auctions, 'biggest_bids': biggest_bids})
    


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")

@login_required
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


def create_auction(request):
    if request.method == "POST":
        form = AuctionForm(request.POST, user=request.user, time=datetime.now())
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = AuctionForm()
    
    context = {'form': form}
    return render(request, 'auctions/new_auction.html', context)

@login_required
def process_bid_form(request, auction):
    if request.method == 'POST':
        form = BidForm(request.POST, user=request.user, auction=auction)
        if form.is_valid():
            bid = form.save(commit=False)
            if bid.value  > bid.biggest_bid(auction):
                bid.save()
                messages.success(request, 'Bid placed successfully.')
            else:
                messages.error(request, 'Your bid must be higher than the current highest bid.')
    else:
        form = BidForm(user=request.user, auction=auction)

    return form

@login_required
def process_comment_form(request, auction):
    if request.method == 'POST':
        form = CommentForm(request.POST, user=request.user, auction=auction)
        if form.is_valid():
            form.save()
    else:
        form = CommentForm(user=request.user, auction=auction)
    return form


def auction_page(request, slug):
    auction = get_object_or_404(Auction, slug=slug)
    comments = Comment.objects.filter(auction=auction)
    bid_form = process_bid_form(request, auction)
    comment_form = process_comment_form(request, auction)
    watchlist = request.user.watchlist.filter(auction=auction) if request.user.is_authenticated else None
    context = {
        'auction': auction,
        'comments': comments,
        'watchlist': watchlist,
        'bid_form': bid_form,
        'comment_form': comment_form,
        }
    return render(request, 'auctions/auction.html', context)


def watchlist(request):
    watchlist = Watchlist.objects.filter(user=request.user)
    return render(request, 'auctions/watchlist.html', {'watchlist': watchlist})


def watchlist_add(request, auction_id):
    if request.user.is_authenticated:
        auction = Auction.objects.get(pk=auction_id)
        if request.user.watchlist.filter(auction=auction).exists():
            return redirect('auction', slug=auction.slug)
        else:
            Watchlist.objects.create(user=request.user, auction=auction)
            return redirect('auction', slug=auction.slug)

    else:
        return redirect('login')
    
def watchlist_remove(request, watchlist_item_id):
    if request.user.is_authenticated:
        watchlist_item = get_object_or_404(Watchlist, pk=watchlist_item_id)
        auction = watchlist_item.auction
        if watchlist_item.user == request.user:
            watchlist_item.delete()
        return redirect('auction', slug=auction.slug)
    else:
        return redirect('login')


def close_auction(request, auction_id):
    if request.user.is_authenticated:
        auction = get_object_or_404(Auction, pk=auction_id)
        if auction.user == request.user:
            if Bid.objects.filter(auction=auction).exists():
                winner = Bid.winner_bid(auction).user
            else:
                winner = None
            auction.close_auction(winner)
            auction.save()
            return redirect('auction', slug=auction.slug)
            


    else:
        return redirect('login')
    

def category_list(request):
    categories = Category.objects.all()
    return render(request, 'auctions/categories.html', {'categories': categories})

def auction_list_by_category(request, category_id):
    category = Category.objects.get(pk=category_id)
    auctions = Auction.objects.filter(category=category)
    return render(request, 'auctions/auction_list_by_category.html', {'category': category, 'auctions': auctions})