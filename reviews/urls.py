from django.urls import path

from . import views

app_name = 'reviews'

urlpatterns = [
    path('review/',
         views.ReviewListView.as_view(), name='review'),
    path('add_review/',
         views.ReviewCreateView.as_view(), name='add_review'),
    path('update_review/<int:pk>/', views.UpdateReviewView.as_view(),
         name='update_review'),
    path('delete_review/<int:pk>/', views.DeleteReviewView.as_view(),
         name='delete_review'),
]
