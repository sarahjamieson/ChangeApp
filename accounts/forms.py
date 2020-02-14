from django import forms
from django.contrib.auth.forms import UserCreationForm

from accounts.models import User
from db.models import Hub


class SemanticMCF(forms.ModelMultipleChoiceField):
    """Class to allow for multiple choice dropdowns to render correctly.

    In Semantic UI, multiple dropwdown <select> object get their placeholder
    value from an included option with value="" ie <select><option value=""> ..
    However the Django default ModelMultipleChoiceField does not allow for
    creation of this as with other Fields as the inherited value empty_label is
    set to None. By overriding this value after the __init__ call we can use
    the django form to full potential to render form without need for extensive
    JS.
    """
    def __init__(self, queryset, empty_label, **kwargs):
        super(SemanticMCF, self).__init__(queryset, **kwargs)
        self.empty_label = empty_label


class CustomUserCreationForm(UserCreationForm):
    """Form containing all necessary modifiable user fields.
    """
    email = forms.EmailField(
        max_length=254,
        required=True
    )
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
    hubs = SemanticMCF(
        queryset=Hub.objects.all(),
        label='Hub(s)',
        empty_label="Hub or Section",
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
        self.fields['band'].choices = [('', 'Band')] + [
            # don't allow 'not set' in form
            band_choice for band_choice in band_choices
            if band_choice[0] != 'N'
        ]
        self.fields['hubs'].choices.empty_label = 'Hub'


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
    """Form allowing editing of certain user fields - not username.

    Since this inherits from a UserCreationForm (grandparent) must not provide
    password fields either which are included by default.
    """
    def __init__(self, *args, **kwargs):
        super(UpdateProfileForm, self).__init__(*args, **kwargs)
        del self.fields['password1']
        del self.fields['password2']

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        if commit:
            user.save()
        return user


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
