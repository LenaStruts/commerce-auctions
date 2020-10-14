from django.urls import path

from . import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("listing/<int:pk>/", views.listing_detail, name='listing_detail'),
    path("listing/new/", views.new_listing, name='new_listing'),
    path("listing/<int:pk>/comment/", views.add_comment, name='add_comment'),
    path("categories", views.categories, name="categories"), 
    path("category/<str:category>", views.category, name="category"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("listing/<int:pk>/watchlist_add/", views.watchlist_add, name="watchlist_add"),
    path("listing/<int:pk>/watchlist_remove/", views.watchlist_remove, name="watchlist_remove"),
    path("listing/<int:pk>/bid/", views.bid, name="bid"),
    path("listing/<int:pk>/close", views.close, name="close"),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
