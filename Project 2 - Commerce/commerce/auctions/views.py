from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms
from datetime import date
from django.db.models import Max
from .models import User, Listing, Bid, Comment, Category, Watchlist



def get_current_price(listing_id):
    listing = Listing.objects.all().get(pk=int(listing_id))
    if listing.bids.all():
        current_price = listing.bids.all().order_by('-price').first().price
        return current_price
    else:
        return listing.starter_price



#------------------FORMS------------------

class NewComment(forms.Form):
    comment = forms.CharField(max_length=255, label='Leave comment', widget = forms.Textarea)


class NewListing(forms.Form):
    title = forms.CharField(max_length=25, label='Title')
    description = forms.CharField(max_length=150, label='desctiption', widget = forms.Textarea)
    categories = []
    for category in Category.objects.all():
        categories.append(tuple([str(category.id), category.name]))
    category = forms.ChoiceField(choices=categories)
    starter_price = forms.IntegerField()
    image = forms.CharField(max_length=255, required=False)


class NewBid(forms.Form):
    price = forms.IntegerField(label='', widget=forms.NumberInput(attrs={'min' : 0, 'placeholder': 'Bid Amount'}))


#--------PLACE BID----------


def place_bid(request, listing_id):
    if request.method == 'POST':
        bid_form = NewBid(request.POST)
        listing = Listing.objects.get(pk=listing_id)
        if bid_form.is_valid():
            bid_price = bid_form.cleaned_data['price']
            if bid_price > get_current_price(listing.id):
                bid = Bid(lot = listing, bidder=request.user, price=bid_price)
                bid.save()
                listing.current_price = bid_price
                listing.save()
                return HttpResponseRedirect(reverse('view_listing', args=[listing_id]))
            else:
                return HttpResponseRedirect(reverse('view_listing', args=[listing_id]))



#---------INDEX PAGE------------

def index(request):
    listings = reversed(Listing.objects.all().filter(active=True))
    return render(request, "auctions/index.html", {
        'listings': listings,
    })



#---------LISTING PAGE------------

def view_listing(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    comment_form = NewComment()
    comments = reversed(listing.comments.all())
    bid_form = NewBid()
    user = request.user

    listing_context = {'listing': listing,
                        'comment_form': comment_form,
                        'comments': comments,
                        'bid_form': bid_form,
                        }

    if user.is_authenticated:
        in_watchlist = listing in [x.listing for x in user.watchlist.all()]
        listing_context['in_watchlist'] = in_watchlist

    if listing.bids.all():
        current_bid = listing.bids.all().order_by('-price').first()
        listing_context['current_bid'] = current_bid

    return render(request, 'auctions/listing.html', listing_context)



#---------CREATE LISTING------------

def new_listing(request):
    if request.method == 'POST':
        listing_form = NewListing(request.POST)
        if listing_form.is_valid():
            title = listing_form.cleaned_data['title']
            description = listing_form.cleaned_data['description']
            category = Category.objects.all().get(pk=int(listing_form.cleaned_data['category']))
            seller = request.user
            starter_price = listing_form.cleaned_data['starter_price']
            image = listing_form.cleaned_data['image']
            date_listed = date.today()
            listing = Listing(title=title, description=description, category=category, seller=seller, starter_price=starter_price, image=image, date_listed=date_listed, current_price=starter_price)
            listing.save()
    
    listing_form = NewListing()
    seller = request.user
    return render(request, 'auctions/new_listing.html', {
        'listing_form': listing_form,
        'seller': seller
    })



def close_listing(request, listing_id):    
    if request.method == 'POST':
        listing = Listing.objects.all().get(pk=listing_id)
        if listing.bids.all():
            final_bid = listing.bids.all().order_by('-price').first()
            final_bid.final = True
            final_bid.save()
        listing.active = False
        listing.save()    
        return HttpResponseRedirect(reverse('view_listing', args=[listing_id]))
        


#---------LEAVE COMMENT------------

def leave_comment(request, listing_id):
    if request.method == 'POST':
        comment_form = NewComment(request.POST)
        if comment_form.is_valid():
            text = comment_form.cleaned_data['comment']
            author = request.user
            listing = Listing.objects.all().get(pk=listing_id)

            comment = Comment(comment=text, author=author, listing=listing)
            comment.save()
            return HttpResponseRedirect(reverse('view_listing', args=[listing.id]))



#---------WATCHLIST PAGE------------

def watchlist(request):
    user = request.user
    watchlist = reversed(user.watchlist.all())
    return render(request, 'auctions/watchlist.html', {
        'watchlist': watchlist
    })


def watchlist_add(request, listing_id):
    if request.method == 'POST':
        user = request.user
        listing = Listing.objects.all().get(pk=int(listing_id))
        current_wathlist = [x.listing for x in user.watchlist.all()]
        if listing not in current_wathlist:
            watchlist = Watchlist(user=user, listing=listing)
            watchlist.save()
            return HttpResponseRedirect(reverse('view_listing', args=[listing_id]))
        else:
            return HttpResponse('ERROR')


def watchlist_remove(request, listing_id):
    user = request.user
    watchlist_item = user.watchlist.all().get(listing=int(listing_id))
    watchlist_item.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))



#----------MY LISTINGS-------------

def my_listings(request):
    user = request.user
    active_listings = reversed(user.listings.all().filter(active=True))
    inactive_listings = reversed(user.listings.all().filter(active=False))
    return render(request, 'auctions/my_listings.html', {
        'active_listings': active_listings,
        'inactive_listings': inactive_listings
    })




#---------AUTHORIZATION------------


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

