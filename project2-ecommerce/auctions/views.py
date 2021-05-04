from typing import List
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.messages.api import add_message
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .utils import BidForm, CommentForm, ListingForm
from .models import Bid, User, Listing, Comment


def index(request):
    return render(request, 'auctions/auction_listing.html', {
        "auctions": Listing.objects.all()
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


def create_listing(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = ListingForm(request.POST)
            if form.is_valid():
                try:
                    new_listing = form.save(commit=False)
                    assert request.user.is_authenticated
                    new_listing.user = request.user
                    new_listing.save()
                    messages.success(request, 'Hoorray! Your new item has been create!')
                    # user = request.user
                    # title = form.cleaned_data['title']
                    # description = form.cleaned_data['description']
                    # starting_bid = form.cleaned_data['starting_bid']
                    # image_url = form.cleaned_data['image_url']
                    # category = form.cleaned_data['category']
                    # new_listing = Listing.objects.create(user=user, title=title, description=description, starting_bid=starting_bid,
                    #                                     image_url=image_url, category=category)
                    # new_listing.save()
                    return HttpResponseRedirect(reverse('index'))
                except ValueError:
                    print("WRONG")

        return render(request, 'auctions/create_listing.html', {
            "form": ListingForm()
        })
    
    else:
        return render(request, 'auctions/create_listing.html', {
            'not_an_user': True
        })


def auction_listing(request):

    return render(request, 'auctions/auction_listing.html', {
        "auctions": Listing.objects.all()
    })


def show_listing(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    try:
        watched_id =  request.user.watchlist.get(pk=listing_id)
    except Exception as e:
        watched_id = None

    if listing.user == request.user:
        user_creator = True
    else:
        user_creator = None
    if request.method == 'POST':
        request.user.watchlist.add(listing)
        print(f'{listing} has been added to {request.user}')
        return HttpResponseRedirect(reverse('show_listing', args=(listing_id,)))

    return render(request, 'auctions/show_listing.html', {
        'listing': listing,
        'watched_id': watched_id,
        'comments': Comment.objects.all(),
        'user_creator': user_creator
    })


def watchlist(request):
    if request.user.is_authenticated:
        return render(request, 'auctions/watchlist.html', {
            'listings': request.user.watchlist.all()
        })
    else:
        return render(request, 'auctions/watchlist.html', {
            'not_an_user': True
        })


@login_required
def comment_listing(request, listing_id):
    listing_commented = Listing.objects.get(pk=listing_id)
    form = CommentForm(request.POST)
    try:
        if request.method == 'POST' and form.is_valid():
            new_comment = form.cleaned_data['comment']
            add_comment = Comment()
            add_comment.writer = request.user
            add_comment.listing = listing_commented
            add_comment.comment = new_comment
            add_comment.save()
            messages.success(request, 'Hoorray! Your new comment has been posted!')
            return HttpResponseRedirect(reverse('show_listing', args=(listing_id,)))
        else:
            print('Error')

    except Exception as e:
        print(e)
    
    return HttpResponseRedirect(reverse('show_listing', args=(listing_id,)))


def categories(request):
    categories = list(set([listing.get_category_display() for listing in Listing.objects.all() if listing.category]))
    for i in Listing.objects.all():
        print(i.get_category_display())
    return render(request, 'auctions/categories.html', {
        'categories': categories,
        'listings': Listing.objects.all()
    })


@login_required
def close_auction(request, listing_id):
    if request.method == 'POST':
        listing = Listing.objects.get(pk=listing_id)
        if request.user == listing.user:
            listing.closed = True
            listing.save()
    
    return HttpResponseRedirect(reverse('show_listing', args=(listing_id,)))


@login_required
def make_a_bid(request, listing_id):
    # form = BidForm(request.POST['offer'])
    offer = float(request.POST['offer'])
    listing_bidded = Listing.objects.get(pk=listing_id)
    if request.method == 'POST' : #and offer.is_valid()
        request.user.buyer.add(listing_bidded)
        listing_bidded.current_bid = offer
        listing_bidded.save()

        bid = Bid()
        bid.bidder = request.user
        bid.listing = listing_bidded
        bid.active_bid = offer
        bid.save()
        messages.success(request, 'Hoorray! Your bid has been saved!')
        return HttpResponseRedirect(reverse('show_listing', args=(listing_id,)))

    return HttpResponseRedirect(reverse('show_listing', args=(listing_id,)))

@login_required
def remove_from_watchlist(request, listing_id):
    obj_to_remove = Listing.objects.get(pk=listing_id)
    if request.method == 'POST':
        obj_to_remove.watchlist.remove(request.user)

        return HttpResponseRedirect(reverse('show_listing', args=(listing_id,)))
