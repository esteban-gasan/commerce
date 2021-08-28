from django import forms
from django.forms import widgets
from django.forms.models import ModelForm
from django.utils.translation import gettext_lazy as _

from .models import Comment, Item

form_control = {'class': 'form-control'}  # Bootstrap class


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)
        labels = {
            'text': False
        }
        widgets = {
            'text': forms.Textarea(attrs=form_control | {'rows': 3})
        }


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
