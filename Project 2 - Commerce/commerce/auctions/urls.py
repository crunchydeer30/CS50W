from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path('listings/<int:listing_id>', views.view_listing, name='view_listing'),
    path('listings/<int:listing_id>/comment', views.leave_comment, name='leave_comment'),
    path('new_listing', views.new_listing, name='new_listing'),
    path('watchlist', views.watchlist, name='watchlist'),
    path('listing/<int:listing_id>/wathclist_add', views.watchlist_add, name='watchlist_add'),
    path('watchlist/remove/<int:listing_id>', views.watchlist_remove, name='watchlist_remove'),
    path('listing/<int:listing_id>/place_bid', views.place_bid, name='place_bid'),
    path('listing/<int:listing_id>/close', views.close_listing, name='close_listing'),
    path('my_listings', views.my_listings, name='my_listings')
]
