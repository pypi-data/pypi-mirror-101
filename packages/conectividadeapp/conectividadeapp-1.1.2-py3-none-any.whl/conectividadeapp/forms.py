from django import forms
from django.forms import ModelForm
from .models import  Actor
from utilities.forms import BootstrapMixin

BLANK_CHOICE = (("", "---------"),)

class ActorForm(BootstrapMixin, ModelForm):
    class Meta:
        model = Actor
        fields = ['name', 'category', 'telephone', 'cellphone', 'email']


class ActorFilterForm(BootstrapMixin, forms.ModelForm):
    q = forms.CharField(
        required=False,
        label="Search",
    )

    class Meta:
        model = Actor
        fields = [
            'q',
        ]