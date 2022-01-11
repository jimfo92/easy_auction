from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("new_listing/", views.new_listing, name="new_listing"),
    path("auction_details/<int:auction_id>/", views.auction_details, name="auction_details"),
    path("make_bid/<int:auction_id>", views.make_bid, name="make_bid"),
    path("add_to_watchlist/<int:auction_id>/", views.add_watchlist, name="add_watchlist"),
    path("delete_from_watchlist/<int:auction_id>/", views.delete_watchlist, name="delete_watchlist"),
    path("delete_auction/<int:auction_id>", views.delete_auction, name="delete_auction"),
    path("watchlist/", views.watchlist, name="view_watchlist"),
    path("add_commet/<int:auction_id>", views.add_commet, name="add_commet"),
    path("categories/", views.categories, name="categories"),
    path("categories/<str:ct>", views.category_items, name="category_items")
    ]
