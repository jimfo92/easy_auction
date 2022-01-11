from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms

from .models import Commet, User,Auctions, Watchlist, Bids
from django.contrib.auth.decorators import login_required


class newListing(forms.Form):
    title = forms.CharField(label="Title")
    description = forms.CharField(widget=forms.Textarea, label="Description")
    starting_bid = forms.IntegerField(label="Starting Bid")
    url = forms.URLField(label="image url", required=False)
    category = forms.CharField(label="Category", required=False)


class bid_form(forms.Form):
    your_bid = forms.IntegerField(label="Your Bid")


class commets(forms.Form):
    commet = forms.CharField(widget=forms.Textarea, label="Write Something")


def index(request):
    list_of_active_auctions = []
    auctons = Auctions.objects.filter(is_active = True)

    for au in auctons:
        auction = Bids.objects.get(auction = au)
        list_of_active_auctions.append(auction)
    list_of_active_auctions.reverse()

    return render(request, "auctions/index.html", {
        "auctions":list_of_active_auctions, "active":True
    })


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


def new_listing(request):
    if request.method == "POST":
        form_listing = newListing(request.POST)
        if form_listing.is_valid():
            title_auction = form_listing.cleaned_data["title"]
            description_auction = form_listing.cleaned_data["description"]
            starting_bid_auction = form_listing.cleaned_data["starting_bid"]
            url_image_auction = form_listing.cleaned_data["url"]
            category_auction = form_listing.cleaned_data["category"]
            auction_item = Auctions(name=title_auction, description=description_auction, image_url=url_image_auction, category=category_auction, user_created_auction=request.user)
            auction_item.save()
            bid = Bids(starting_bid=starting_bid_auction, auction=auction_item)
            bid.save()

            return HttpResponseRedirect(reverse("index"))

    return render(request, "auctions/new_listing.html", {
        "listing_form":newListing()
    })


def auction_details(request, auction_id):
    #Find auction details, bid for the auction and auction commets
    auction_item = Auctions.objects.get(pk = auction_id)
    bid_for_auction = Bids.objects.get(auction = auction_item)
    commets_list = Commet.objects.filter(auction=auction_item)

    if not request.user.is_authenticated:
        return render(request, "auctions/auction_details.html", {
        "item":bid_for_auction, "form":bid_form(), "commets":commets_list
        })

    # user is authenticated
    try:
        watchlist_item = Watchlist.objects.get(user=request.user, auction=auction_item)
    except Watchlist.DoesNotExist:
        watchlist_item = None    
    isUser = auction_item.user_created_auction == request.user

    return render(request, "auctions/auction_details.html", {
        "item":bid_for_auction, "is_watchlist":watchlist_item,
        "form":bid_form(), "user_created_auction":isUser, 
        "commets":commets_list
    })


@login_required
def make_bid(request, auction_id):
    # auction deatails and auctions bids
    auction_item = Auctions.objects.get(pk = auction_id)
    bid_for_auction = Bids.objects.get(auction = auction_item)
    commets_list = Commet.objects.filter(auction=auction_item)

    if request.method=="POST":
        new_bid = bid_form(request.POST)
        if new_bid.is_valid():
            bid = new_bid.cleaned_data["your_bid"]
            if (bid > bid_for_auction.last_bid and bid > bid_for_auction.starting_bid):
                bid_for_auction.last_bid = bid
                bid_for_auction.user_who_made_last_successful_bid = request.user
                bid_for_auction.save()
                return HttpResponseRedirect(reverse('auction_details', args=[auction_id]))
            wrong_bid = True
            try:
                watchlist_item = Watchlist.objects.get(user=request.user, auction=auction_item)
            except Watchlist.DoesNotExist:
                watchlist_item = None    
            isUser = auction_item.user_created_auction == request.user
            return render(request, "auctions/auction_details.html", {
                "is_watchlist":watchlist_item, "form":bid_form(), 
                "item":bid_for_auction, "user_created_auction":isUser, 
                "commets":commets_list, "wrong_bid":wrong_bid
            })


@login_required
def add_watchlist(request, auction_id):
    auction_item = Auctions.objects.get(pk=auction_id)
    item = Watchlist(user=request.user, auction=auction_item)
    item.save()
    
    return HttpResponseRedirect(reverse('auction_details', args=[auction_id]))


@login_required
def delete_watchlist(request, auction_id):
    auction_item = Auctions.objects.get(pk=auction_id)
    entry= Watchlist.objects.get(user=request.user ,auction=auction_item)
    entry.delete()

    return HttpResponseRedirect(reverse('auction_details', args=[auction_id]))


def delete_auction(request, auction_id):
    auction = Auctions.objects.get(id = auction_id)
    auction.is_active = False
    auction.save()

    return HttpResponseRedirect(reverse('index'))


def watchlist(request): 
    watchlist_items = Watchlist.objects.filter(user=request.user)
    active_items = []
    in_active_items = []
    for item in watchlist_items:
        if item.auction.is_active == True:
            active_items.append(item)
        else:
            in_active_items.append(item)

    bids_for_watchlist_items = []
    bids_non_active_items = []
    for item in active_items:
        bid = Bids.objects.get(auction=item.auction)
        bids_for_watchlist_items.append(bid)
    for item in in_active_items:
        bid = Bids.objects.get(auction=item.auction)
        bids_non_active_items.append(bid)

    return render(request, "auctions/index.html", {
        "auctions":bids_for_watchlist_items, "inactive_auctions":bids_non_active_items,
         "watchlist":True
    })


@login_required
def add_commet(request, auction_id):
    if request.method != "POST":
        return HttpResponseRedirect(reverse('auction_details', args=[auction_id]))
    auction_item = Auctions.objects.get(pk=auction_id)
    commet_item = request.POST.get('commet')  
    print(commet_item)
    cm = Commet(commet=commet_item, user=request.user, auction=auction_item)
    cm.save()  

    return HttpResponseRedirect(reverse('auction_details', args=[auction_id]))


def categories(request):
    categories_set = set(Auctions.objects.values_list('category', flat=True))
    
    return render(request, "auctions/categories.html", {
        "categories":categories_set
    })


def category_items(request, ct):
    category_items = Auctions.objects.filter(category=ct, is_active=True)
    inactive_items = Auctions.objects.filter(category=ct, is_active=False)
    auctions = []
    inactive_auctions = []
    for item in category_items:
        bid_item = Bids.objects.get(auction=item)
        auctions.append(bid_item)
    for item in inactive_items:
        bid_item = Bids.objects.get(auction=item)
        inactive_auctions.append(bid_item)

    return render(request, "auctions/index.html", {
        "auctions":auctions, "inactive_auctions":inactive_auctions, "category":ct
    })