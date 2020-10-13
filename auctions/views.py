from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from .models import Listing, Comment, Watchlist, Bid, User
from .forms import ListingForm, CommentForm, BidForm
from django.utils import timezone
from django.db.models import Max
from django.contrib import messages


def index(request):
    listings = Listing.objects.all()
    return render(request, "auctions/index.html", {'listings': listings})



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


def listing_detail(request, pk):
    listing = get_object_or_404(Listing, pk=pk)
    listing_bids = Bid.objects.filter(listing=listing)
    if listing.active == False:
        max_bid = Bid.objects.filter(listing=listing).order_by('-bids')[0]
        winner = max_bid.user
        current_user = request.user
        if current_user == winner:
            return render(request, "auctions/listing_detail.html", {
                'listing': listing,
                'is_winner': True
            })
        else:
            return render(request, "auctions/listing_detail.html", {
                'listing': listing,
                'listing_bids': listing_bids,
            })
    else:
        listing_user = request.user
        if Watchlist.objects.filter(user=listing_user, listing=listing).exists():
            listing_added = True
        else:
            listing_added = False
        return render(request, "auctions/listing_detail.html", {
            'listing': listing,
            'listing_bids': listing_bids,
            'listing_added': listing_added
        })


def new_listing(request):
    if request.method == "POST":
        form = ListingForm(request.POST)
        if form.is_valid():
            listing = form.save(commit=False)
            listing.user = request.user
            listing.date_created = timezone.now()
            listing.save()
            return redirect('listing_detail', pk=listing.pk)
    else:
        form = ListingForm()
    return render(request, "auctions/edit.html", {'form': form})


def add_comment(request, pk):
    listing = get_object_or_404(Listing, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.listing = listing
            comment.user = request.user
            comment.published_date = timezone.now()
            comment.save()
            return redirect('listing_detail', pk=listing.pk)
    else:
        form = CommentForm()
    return render(request, "auctions/add_comment.html", {'form': form})


def categories(request):
    categories = Listing.Categories
    return render(request, "auctions/categories.html", {"categories": categories})

def category(request, category):
    cat_listings = Listing.objects.filter(category=category)
    return render(request, "auctions/category.html", {"cat_listings": cat_listings})

def watchlist(request):
    watchlist = Watchlist.objects.filter(user=request.user)
    return render(request, "auctions/watchlist.html", {"watchlist": watchlist})

def watchlist_add(request, pk):
    listing_to_add = get_object_or_404(Listing, pk=pk)
    if Watchlist.objects.filter(user=request.user, listing=listing_to_add).exists():
        return HttpResponseRedirect(reverse("index"))
    else:
        user_list, created = Watchlist.objects.get_or_create(user=request.user, listing=listing_to_add)
        return render(request, "auctions/watchlist.html")

def watchlist_remove(request, pk):
    listing_to_remove = get_object_or_404(Listing, pk=pk)
    item = Watchlist.objects.filter(user=request.user, listing=listing_to_remove)
    if item.exists():
        item.delete()
        return redirect('listing_detail', pk=listing_to_remove.pk)
    else: 
        return HttpResponseRedirect(reverse("index"))


def bid(request, pk):
    listing_to_bid = get_object_or_404(Listing, pk=pk)
    listing_to_bid_price = listing_to_bid.price
    if request.method == "POST":
        form = BidForm(request.POST)
        if form.is_valid():
            bid = form.save(commit=False)
            bid.listing = listing_to_bid
            bid.user = request.user
            bid.bid_time = timezone.now()
            if int(request.POST.get("bids")) > listing_to_bid.price:
                bid.bids = int(request.POST.get("bids"))
                listing_to_bid.price = bid.bids
                bid.save()
                listing_to_bid.save()
            return redirect('listing_detail', pk=listing_to_bid.pk)
    else:
        form = BidForm()
    return render(request, "auctions/bid.html", {'form': form})  


def close(request, pk):
    listing_to_close = get_object_or_404(Listing, pk=pk)
    logged_user = request.user
    if logged_user == listing_to_close.user:
        listing_to_close.active = False
        listing_to_close.save()
    return HttpResponseRedirect(reverse("index"))