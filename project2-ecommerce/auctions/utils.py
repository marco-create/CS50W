from django.db.models import fields
from .models import Listing, Comment, Bid
from django.forms import ModelForm

class ListingForm(ModelForm):
    class Meta:
        model = Listing
        fields = ['title',
        'starting_bid',
        'image_url',
        'category',
        'description']

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['comment']

class BidForm(ModelForm):
    class Meta:
        model = Bid
        fields = ['active_bid']