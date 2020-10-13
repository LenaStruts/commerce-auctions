from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    pass

class Listing(models.Model):

    class Categories(models.TextChoices):
        FASHION = 'Fashion', _('Fashion')
        ELECTRONICS_MEDIA = 'Electronics_Media', _('Electronics & Media')
        TOYS_HOBBY_DIY = 'Toys_Hobby_DIY', _('Toys, Hobby & DIY')
        FURNITURE_APPLIANCES = 'Furniture_Appliances', _('Furniture & Appliances')
        FOOD_CARE = 'Food_Care', _('Food & Personal Care')

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=9, decimal_places=2)
    date_created = models.DateTimeField(default=timezone.now)
    watchlist = models.ManyToManyField(User, through='Watchlist', related_name='listings_on_watchlist')
    listing_bids = models.ManyToManyField(User, through='Bid', related_name='listing_bidded')
    image = models.CharField(max_length=1000, default="", blank=True)
    category = models.CharField(max_length=64, blank=True, choices=Categories.choices)
    active = models.BooleanField(default=True)

class Watchlist(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='listings_for_watchlist')

class Bid(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='listing_to_bid')
    bid_time = models.DateTimeField(default=timezone.now)
    bids = models.DecimalField(max_digits=9, decimal_places=2)

class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    listing = models.ForeignKey('auctions.Listing', on_delete=models.CASCADE, related_name='comments')
    message = models.TextField()
    published_date = models.DateTimeField(default=timezone.now)
