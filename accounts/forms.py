from django import forms
from django.contrib.auth.forms import UserCreationForm

from accounts.models import User
from db.models import Hub


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(max_length=254, required=True)
    first_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'First Name'
            }
        )
    )
    last_name = forms.CharField(
        max_length=150,
        required=True,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Last Name'
            }
        )
    )
    role = forms.CharField(
        max_length=80,
        required=True,
        label='Role',
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Job Title or Role'
            }
        )
    )
    band = forms.ChoiceField(
        choices=User.Band.choices,
        widget=forms.Select(
            attrs={
                'class': 'ui dropdown'
            }
        )
    )
    hubs = forms.ModelMultipleChoiceField(
        queryset=Hub.objects.all(),
        label='Hub(s)',
        required=True,
        widget=forms.SelectMultiple(
            attrs={
                'class': 'ui dropdown',
            }
        )
    )

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        band_choices = self.fields['band'].choices
        hub_choices = self.fields['hubs'].choices
        print(hub_choices)
        self.fields['band'].choices = [('', 'Band')] + band_choices


    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'username',
            'email',
            'band',
            'hubs',
            'role'
        )


class UpdateProfileForm(CustomUserCreationForm):
    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'email',
            'band',
            'hubs',
            'role',
        )
