from django.urls import include
from django.urls import path

from accounts import views


urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('profile/<str:username>', views.ProfileView.as_view(), name='profile')
]
