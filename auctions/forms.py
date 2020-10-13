from django import forms

from .models import Listing, Comment, Bid

class ListingForm(forms.ModelForm):

    class Meta:
        model = Listing
        fields = ('title', 'description', 'price', 'image', 'category')


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('message',)


class BidForm(forms.ModelForm):
     
    class Meta:
        model = Bid
        fields =('bids',)
