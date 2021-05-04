from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

class User(AbstractUser):
    pass

class Listing(models.Model):
    title = models.CharField(max_length=64, help_text='Provide the name of the new item.')
    description = models.CharField(max_length=255, help_text='Add a short description of the item.')
    starting_bid = models.FloatField(help_text='Set the initial bid.')
    current_bid = models.FloatField(null=True, blank=True)
    image_url = models.URLField(blank=True, help_text='Optional. Provide an "url" for an image for the listing.')
    category = models.CharField(max_length=64, choices=(('1','Fashion'),('2','Toys'),('3','Electronics'),('4','Home'),), help_text='Choose a category.')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')
    date = models.DateTimeField(editable=False, default=timezone.now)
    closed = models.BooleanField(default=False)

    watchlist = models.ManyToManyField(User, blank=True, related_name='watchlist')
    buyer = models.ManyToManyField(User, null=True, related_name='buyer')

class Bid(models.Model):
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bidder')
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='bidded_listing')
    active_bid = models.FloatField(null=True, blank=True)


class Comment(models.Model):
    writer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='writer')  
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='listing') 
    comment = models.CharField(max_length=64)
    date = models.DateTimeField(editable=False, default=timezone.now)

