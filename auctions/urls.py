from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("auctions/<slug:slug>", views.auction_page, name="auction"),
    path("new-auction", views.create_auction, name="new_auction"),
    path('watchlist/', views.watchlist, name='watchlist'),
    path('watchlist/add/<int:auction_id>', views.watchlist_add, name='watchlist_add'),
    path('watchlist/remove/<int:watchlist_item_id>', views.watchlist_remove, name='watchlist_remove'),
    path('close-auction/<int:auction_id>', views.close_auction, name='close_auction'),
]
