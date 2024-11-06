from django.urls import path

from . import views

app_name = 'pages'

urlpatterns = [
    path('', views.IndexPage.as_view(), name='index'),
    path('price/', views.PriceListView.as_view(), name='price'),
    path('foto/', views.FotoPage.as_view(), name='foto'),
    path('contact/', views.ContactPage.as_view(), name='contact'),
    path('info/', views.InfoPage.as_view(), name='info'),
    path('info/<int:id>/', views.DetailInfoPage.as_view(), name='detail_info'),
]
