from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.db.models.aggregates import Max
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from .forms import BidForm, CommentForm, ItemForm
from .models import Category, Item, User


def index(request):
    i = Item.objects.filter(active=True).annotate(
        highest_bid=Max("bids__bid_amount"))
    a = i[0].highest_bid
    b = i[1].highest_bid
    context = {
        "items": Item.objects.filter(active=True),
        "empty_msg": "There are no active listings."
    }
    return render(request, "auctions/index.html", context)


def item_view(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    context = {
        "item": item,
        "categories": item.categories.all(),
        "bids": item.bids.all(),
        "bids_count": item.bids.count(),
        "highest_bid": item.bids.order_by("-bid_amount").first(),
        "comments": item.comments.all(),
        "bid_form": BidForm(),
        "comment_form": CommentForm(),
    }

    if request.method != "POST":
        return render(request, "auctions/item.html", context)

    if not request.user.is_authenticated:
        return redirect("auctions:login")  # TODO: con next

    # Check which form was submitted
    if "post-comment" in request.POST:
        comment_form = CommentForm(request.POST)
        if not comment_form.is_valid():
            # Send back the form submitted if errors are found
            context["comment_form"] = comment_form
            return render(request, "auctions/item.html", context)

        # Create object but don't save to the database yet
        new_comment = comment_form.save(commit=False)
        new_comment.author = request.user
        new_comment.posted_on = item
        new_comment.save()              # Save the instance

    elif "place-bid" in request.POST:
        bid_form = BidForm(data=request.POST, item_id=item_id)
        if not bid_form.is_valid():
            # Send back the form submitted if errors are found
            context["bid_form"] = bid_form
            return render(request, "auctions/item.html", context)

        new_bid = bid_form.save(commit=False)
        new_bid.bidder = request.user
        new_bid.item = item
        new_bid.save()

    # User will be redirect after successfully submitting a form
    return redirect("auctions:item", item_id=item_id)


def all_categories(request):
    return render(request, "auctions/all_categories.html", {
        "categories": Category.objects.all()
    })


def category_view(request, category_id):
    context = {
        "category": Category.objects.get(pk=category_id),
        "items": Item.objects.filter(categories=category_id, active=True),
        "empty_msg": "No active items for this category."
    }
    return render(request, "auctions/category.html", context)


@login_required(redirect_field_name=None)
def sell_view(request):
    if request.method == "POST":
        form = ItemForm(request.POST)
        if not form.is_valid():
            return render(request, "auctions/sell.html", {"form": form})

        # Create object but don't save to the database yet
        new_item = form.save(commit=False)
        new_item.seller = request.user
        new_item.save()     # Save the instance
        form.save_m2m()     # Save the many to many data
        return redirect("auctions:item", item_id=new_item.id)

    # GET method
    return render(request, "auctions/sell.html", {"form": ItemForm()})


@login_required(redirect_field_name=None)
def watchlist(request):
    context = {
        "items": request.user.watchlist.all(),
        "empty_msg": "You haven't added items to your watchlist."
    }
    return render(request, "auctions/watchlist.html", context)


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("auctions:index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("auctions:index"))


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
        return HttpResponseRedirect(reverse("auctions:index"))
    else:
        return render(request, "auctions/register.html")
