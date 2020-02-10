from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.views.generic import DetailView

from accounts.models import User
from accounts.forms import CustomUserCreationForm


class ProfileView(DetailView):
    """User profile view
    """
    model = User
    template_name = 'accounts/profile.html'

    def get_object(self):
        return get_object_or_404(User, username=self.kwargs.get('username'))


class RegisterView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('index')

    def post(self, request):
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            form.save_m2m()
            print(user.hubs.all())
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password1']
            )
            login(request, user)
            messages.info(
                request,
                "Thanks for registering. You are now logged in."
            )
            return render(request, 'index.html')
        else:
            return render(request, self.template_name, {'form': form})
