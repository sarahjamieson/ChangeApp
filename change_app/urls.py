from django.urls import include
from django.urls import path

from change_app import views


urlpatterns = [
    path('suggest', views.SuggestView.as_view(), name='suggest'),
]
