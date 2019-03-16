from django import forms
from .models import Profile


class profileForm(forms.ModelForm):
    class Meta:
        model = Profile
        # exclude user from from so an input is not
        # rendered by the template language
        # we will manually ad the user in the view file
        exclude = ['user']