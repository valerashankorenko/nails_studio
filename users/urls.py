from django.urls import path

from . import views

app_name = 'users'

urlpatterns = [
    path('auth/registration/', views.ProfileCreateView.as_view(),
         name='registration'),
    path('profile/<str:username>/',
         views.ProfileDetailView.as_view(), name='profile'),
    path('edit_profile/',
         views.ProfileUpdateView.as_view(), name='edit_profile'),
]
