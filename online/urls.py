from django.urls import path

from . import views

app_name = 'online'

urlpatterns = [
    path('add_online_rec/',
         views.OnlineRecCreateView.as_view(),
         name='add_online_rec'),
    path('update_online_rec/<int:pk>/',
         views.OnlineRecUpdateView.as_view(),
         name='update_online_rec'),
    path('delete_online_rec/<int:pk>/',
         views.OnlineRecDeleteView.as_view(),
         name='delete_online_rec'),
    path('get-available-time-slots/',
         views.GetAvailableTimeSlotsView.as_view(),
         name='get_available_time_slots'),
]
