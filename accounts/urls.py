from django.urls import path, include
from django.shortcuts import render

from .views import UserProfileUpdateView, EditProfile, upgrade_to_author


urlpatterns = [
    path('profile/', EditProfile),
    path('<int:pk>/edit_profile', UserProfileUpdateView.as_view(), name='profile_update'),
    path('upgrade_to_author/', upgrade_to_author, name='upgrade_to_author')
]