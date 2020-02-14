from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.urls import reverse
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView
from django.views.generic import DetailView
from django.views.generic import FormView
from django.views.generic.detail import SingleObjectMixin

from accounts.models import User
from accounts.forms import CustomUserCreationForm
from accounts.forms import UpdateProfileForm
from accounts.utils import get_user_audit_log
from db.models import Hub


class ProfileDisplay(LoginRequiredMixin, DetailView):
    """User profile view
    """
    model = User
    context_object_name = 'account'
    template_name = 'accounts/profile.html'

    def get_object(self):
        return get_object_or_404(User, username=self.kwargs.get('username'))

    def get_context_data(self, **kwargs):
        context = super(ProfileDisplay, self).get_context_data(**kwargs)
        account=self.get_object()

        context['form'] = UpdateProfileForm(instance=account)
        context['history'] = get_user_audit_log(user=account)
        return context


class ProfileUpdate(LoginRequiredMixin, SingleObjectMixin, FormView):
    model = User
    context_object_name = 'account'
    form_class = UpdateProfileForm
    template_name = 'accounts/profile.html'

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = UpdateProfileForm(request.POST, instance=self.object)
        if form.is_valid():
            form.save()
            form.save_m2m()
            messages.success(request, "User profile successfully updated.")
        return super(ProfileUpdate, self).post(request, *args, **kwargs)

    def get_object(self):
        return get_object_or_404(User, username=self.kwargs.get('username'))

    def get_success_url(self):
        return reverse('profile', kwargs={'username': self.object.username})


class ProfileView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        view = ProfileDisplay.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = ProfileUpdate.as_view()
        return view(request, *args, **kwargs)


class RegisterView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('index')

    def post(self, request):
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            # required to save the custom hubs many-to-many field this way
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


class HubView(LoginRequiredMixin, DetailView):
    """View of an individual hub
    """
    model = Hub
    context_object_name = 'hub'
    template_name = 'accounts/hub.html'
    def get_object(self):
        return get_object_or_404(Hub, name__iexact=self.kwargs.get('name'))
