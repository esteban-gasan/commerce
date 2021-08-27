from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse

from .forms import ItemForm
from .models import Category, Item, User


def index(request):
    context = {"items": Item.objects.filter(active=True)}
    return render(request, "auctions/index.html", context)


def item_view(request, item_id):
    try:
        item = Item.objects.get(id=item_id)
    except Item.DoesNotExist:
        raise Http404("Item not found.")

    return render(request, "auctions/item.html", {
        "item": item,
        "categories": item.categories.all(),
        "bids": item.bids.all(),
        "comments": item.comments.all()
    })


def all_categories(request):
    return render(request, "auctions/all_categories.html", {
        "categories": Category.objects.all()
    })


def category_view(request, category_id):
    context = {
        "category": Category.objects.get(pk=category_id),
        "items": Item.objects.filter(categories=category_id, active=True)
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
