from django import forms

from .models import Listing, Comment, Bid

class ListingForm(forms.ModelForm):

    class Meta:
        model = Listing
        fields = ('title', 'description', 'starting_bid', 'image', 'category')
