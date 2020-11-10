from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('search', views.ajax_method, name='ajax_method'),
    path('new_record', views.new_record, name= 'new_record')
]
