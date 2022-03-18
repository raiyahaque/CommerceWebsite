from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import User, Listing, Bid, Watchlist, Commentary
from .forms import NewEntryForm

def get_user(request):
    username = request.user.username
    user = User.objects.get(username=username)
    return user

def get_watchlist(request):
    list = []
    user = get_user(request)
    # Get user's watchlist
    watchlist = Watchlist.objects.filter(users=user)
    for item in watchlist:
        # Make sure listing is active
        if item.listing.active == True:
            list.append(item.listing)
    return list

def index(request):
    all_listings = Listing.objects.filter(active=True)
    return render(request, "auctions/index.html", {
        "listings": all_listings
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

@login_required(login_url='/login')
def create_listing(request):
    if request.method == 'POST':
        # gather all of the details about the listing
        new_listing = NewEntryForm(request.POST)
        if new_listing.is_valid():
            title = new_listing.cleaned_data["title"]
            description = request.POST.get("description")
            starting_bid = new_listing.cleaned_data["starting_bid"]
            image_url = new_listing.cleaned_data["image_url"]
            category = new_listing.cleaned_data["category"]
            if category == 'No category':
                category = None
            # get the current user
            user = get_user(request)
            # Create the new listing
            listing = Listing(title=title, description=description, starting_bid=starting_bid, image_url=image_url, category=category, users=user, current_price=starting_bid)
            listing.save()
            all_listings = Listing.objects.all()
            return HttpResponseRedirect(reverse("index"), {
                "listings": all_listings,
        })
    return render(request, "auctions/createListing.html", {
        "form": NewEntryForm()
    })

@login_required(login_url='/login')
def listing_page(request, id):
    message = None
    user = get_user(request)
    # Get all objects in user's watchlist
    watch_list = get_watchlist(request)
    # Get listing object that matches the title and is an active listing
    try:
        listing_object = Listing.objects.get(pk=id, active=True)
    except Listing.DoesNotExist:
        raise Http404("Listing not found.")
    # Get all comments regarding the listing
    comments = Commentary.objects.filter(listing=listing_object)
    if request.method == 'POST':
        new_bid_amount = int(request.POST["bid"])
        try:
            listing = Listing.objects.get(pk=id)
        except Listing.DoesNotExist:
            raise Http404("Listing not found.")
        # Check if new bid is higher than starting_bid and other bids
        if new_bid_amount > listing.current_price:
            # Save current price as new bid amount
            listing.current_price = new_bid_amount
            listing.save()
            # Save new bid in bid class
            new_bid = Bid(bid_amount=new_bid_amount, users=user, listing=listing)
            new_bid.save()

        else:
            message = "Your bid needs to be higher than the current price."
    bids = listing_object.bids.count()
    return render(request, "auctions/listingPage.html", {
        "listing": Listing.objects.get(pk=id, active=True),
        "listing_object": listing_object,
        "list": watch_list,
        "comments": comments,
        "bids": bids,
        "bidding_amount": listing_object.current_price,
        "user": user,
        "message": message
    })

@login_required(login_url='/login')
def watchlist_list(request):
    # Get user's watchlist
    watch_list = get_watchlist(request)
    return render(request, "auctions/watchlist.html", {
        "watchlist": watch_list
    })

@login_required(login_url='/login')
def watchlist_add(request, id):
    if request.method == 'POST':
        user = get_user(request)
        # Get the listing object that the user wants to add to the watchlist
        try:
            item = Listing.objects.get(pk=id, active=True)
        except Listing.DoesNotExist:
            raise Http404("Listing not found.")
        # Create that item as a watchlist object
        watchlist_item = Watchlist(users=user, listing=item)
        watchlist_item.save()
        watch_list = get_watchlist(request)

    return render(request, "auctions/watchlist.html", {
        "watchlist": watch_list
    })

@login_required(login_url='/login')
def watchlist_remove(request, id):
    if request.method == 'POST':
        user = get_user(request)
        try:
            item = Listing.objects.get(pk=id, active=True)
        except Listing.DoesNotExist:
            raise Http404("Listing not found.")
        # Remove the watchlist object
        removed = Watchlist.objects.filter(users=user, listing=item)
        removed.delete()
        watch_list = get_watchlist(request)

    return render(request, "auctions/watchlist.html", {
        "watchlist": watch_list
    })

@login_required(login_url='/login')
def categories(request):
    # Get all of the distinct categories
    all_categories = Listing.objects.values('category').distinct()
    categories_list = []
    for category in all_categories:
        # If category has a value
        if category['category'] != None:
            # Add to empty list of categories
            categories_list.append(category['category'])
    return render(request, "auctions/categories.html", {
        "categories": categories_list
        })

@login_required(login_url='/login')
def category(request, topics):
    # Get all of the listings with that particular category
    items = Listing.objects.filter(category=topics, active=True)
    return render(request, "auctions/category_listings.html", {
        "listings": items
    })

@login_required(login_url='/login')
def commentary(request, id):
    user = get_user(request)
    watch_list = get_watchlist(request)
    try:
        listing = Listing.objects.get(pk=id, active=True)
    except Listing.DoesNotExist:
        raise Http404("Listing not found.")    # Get all comments for the listing
    comments = Commentary.objects.filter(listing=listing)
    bids = listing.bids.count()

    if request.method == 'POST':
        # Get new comment
        comment = request.POST["comment"]
        # Create new comment object
        new_comment = Commentary(comment=comment, users=user, listing=listing)
        new_comment.save()
        comments = Commentary.objects.filter(listing=listing)
    return render(request, "auctions/listingPage.html", {
        "listing": Listing.objects.get(pk=id, active=True),
        "listing_object": listing,
        "list": watch_list,
        "bids": bids,
        "comments": comments,

    })
@login_required(login_url='/login')
def my_listings(request):
    user = get_user(request)
    # Get all of the listings that the user created
    listings = Listing.objects.filter(users=user, active=True)
    return render(request, "auctions/my_listings.html", {
        "listings": listings
    })

@login_required(login_url='/login')
def close_listing(request, id):
    user = get_user(request)
    if request.method == 'POST':
        try:
            listing = Listing.objects.get(pk=id, active=True)
        except Listing.DoesNotExist:
            raise Http404("Listing not found.")
        bids = Bid.objects.filter(listing=listing)
        for bid in bids:
            # Get the highest bid to determine the winner
            if bid.bid_amount == listing.current_price:
                # Winner is highest bidder
                listing.winner = bid.users
        # Close the listing
        listing.active = False
        listing.save()
    return render(request, "auctions/my_listings.html", {
        "listings": Listing.objects.filter(users=user, active=True)
    })

@login_required(login_url='/login')
def closed_listings(request):
    # Return all closed listings
    return render(request, "auctions/closed_listings.html", {
        "listings": Listing.objects.filter(active=False)
    })

@login_required(login_url='/login')
def closed_listings_page(request, id):
    try:
        listing = Listing.objects.get(pk=id, active=False)
    except Listing.DoesNotExist:
        raise Http404("Listing not found.")
    user = get_user(request)
    # If user is signed in on a closed listing page, the page should say the user won the auction
    if listing.winner == user:
        message = "Congratulations! You have won the auction!!"
        return render(request, "auctions/closed_listing_page.html", {
            "listing": listing,
            "message": message
        })
    return render(request, "auctions/closed_listing_page.html", {
        "listing": listing
    })
