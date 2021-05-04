from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("register", views.register, name="register"),
    path("logout", views.logout_view, name="logout"),

    path('create_listing', views.create_listing, name='create_listing'),
    path('auction_listing', views.auction_listing, name='auction_listing'),
    path('show_listing/<int:listing_id>', views.show_listing, name='show_listing'),
    path('watchlist', views.watchlist, name='watchlist'),
    path('comment_listing/<int:listing_id>', views.comment_listing, name='comment_listing'),
    path('categories', views.categories, name='categories'),
    path('close_auction/<int:listing_id>', views.close_auction, name='close_auction'),
    path('make_a_bid/<int:listing_id>', views.make_a_bid, name='make_a_bid'),
    path('remove_from_watchlist/<int:listing_id>', views.remove_from_watchlist, name='remove_from_watchlist')
]
