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
        print(max_bid)
        winner = max_bid.user
        print(winner)
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
        print(listing)
        print(Watchlist.objects.filter(user=listing_user, listing = listing).exists())
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