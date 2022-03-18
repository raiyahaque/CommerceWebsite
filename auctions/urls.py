from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create_listing", views.create_listing, name="create_listing"),
    path("listing_page/<int:id>", views.listing_page, name="listing_page"),
    path("watchlist", views.watchlist_list, name="watchlist_list"),
    path("watchlist/<int:id>", views.watchlist_add, name="watchlist_add"),
    path("watchlist_remove/<int:id>", views.watchlist_remove, name="watchlist_remove"),
    path("categories", views.categories, name="categories"),
    path("categories/<str:topics>", views.category, name="category"),
    path("commentary/<int:id>", views.commentary, name="commentary"),
    path("my_listings", views.my_listings, name="my_listings"),
    path("close_listing/<int:id>", views.close_listing, name="close_listing"),
    path("closed_listings", views.closed_listings, name="closed_listings"),
    path("closed_listings/<int:id>", views.closed_listings_page, name="closed_listings_page")
]
