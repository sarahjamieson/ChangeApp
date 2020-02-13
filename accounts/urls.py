from django.urls import include
from django.urls import path

from accounts import views


urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('profile/<str:username>', views.ProfileView.as_view(), name='profile'),
    path('register', views.RegisterView.as_view(), name='register'),
    path('hub/<str:name>', views.HubView.as_view(), name='hub'),
]
