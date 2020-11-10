from django.urls import path
from hotzone import views

urlpatterns = [
    path('', views.index, name='index'),
    path('add_location', views.add_location, name='add_location'),
    path('list_location', views.list_location, name='list_location'),
]