from django.shortcuts import get_object_or_404
from django.views.generic import DetailView

from accounts.models import User


class ProfileView(DetailView):
    """User profile view
    """
    model = User
    template_name = 'accounts/profile.html'

    def get_object(self):
        return get_object_or_404(User, username=self.kwargs.get('username'))
