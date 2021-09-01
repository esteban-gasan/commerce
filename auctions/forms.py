from django import forms
from django.core.exceptions import ValidationError
from django.db.models.aggregates import Max
from django.forms import widgets
from django.forms.models import ModelForm
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _

from .models import Bid, Comment, Item

form_control = {'class': 'form-control'}  # Bootstrap class


class BidForm(ModelForm):
    class Meta:
        model = Bid
        fields = ('bid_amount',)
        labels = {'bid_amount': False}
        widgets = {'bid_amount': forms.NumberInput(attrs=form_control)}

    def __init__(self, *args, **kwargs):
        self.item_id = kwargs.pop('item_id', None)
        super(BidForm, self).__init__(*args, **kwargs)

    def clean_bid_amount(self):
        bid_amount = self.cleaned_data['bid_amount']
        item = get_object_or_404(Item, id=self.item_id)
        highest_bid = item.bids.aggregate(Max("bid_amount"))
        highest_bid = highest_bid['bid_amount__max']
        # Compare against the starting price if there are no bids
        if bid_amount <= max(highest_bid, item.starting_price):
            return ValidationError(
                _("Your bid must be higher than the current item's price"),
                code='low_bid'
            )
        return bid_amount


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)
        labels = {'text': False}
        widgets = {'text': forms.Textarea(attrs=form_control | {'rows': 3})}


class ItemForm(ModelForm):
    class Meta:
        model = Item
        fields = ('name', 'description', 'starting_price',
                  'image_url', 'categories')
        labels = {
            'name': _('Item name'),
            'image_url': _('Image URL')
        }
        widgets = {
            'name': forms.TextInput(attrs=form_control),
            'description': forms.Textarea(attrs=form_control),
            'starting_price': forms.NumberInput(attrs=form_control),
            'image_url': forms.URLInput(attrs=form_control),
            'categories': forms.CheckboxSelectMultiple
        }
