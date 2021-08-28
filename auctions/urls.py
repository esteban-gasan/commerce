from django.urls import path

from . import views


app_name = "auctions"

urlpatterns = [
    path("", views.index, name="index"),
    path("item/<int:item_id>/", views.item_view, name="item"),
    path("categories/", views.all_categories, name="all_categories"),
    path("category/<int:category_id>/", views.category_view, name="category"),
    path("sell/", views.sell_view, name="sell"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register, name="register"),
    path("user/watchlist/", views.watchlist, name="watchlist"),
]
