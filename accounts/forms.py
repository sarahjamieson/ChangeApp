from django import forms
from django.contrib.auth.forms import UserCreationForm

from accounts.models import User
from db.models import Hub


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(max_length=254, required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=150, required=True)
    band = forms.ChoiceField(choices=User.Band.choices)
    hub = forms.ModelMultipleChoiceField(
        queryset=Hub.objects.all(),
        label='Hub(s)'
    )

    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'username',
            'email',
        )
