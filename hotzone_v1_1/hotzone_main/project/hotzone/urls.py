from django.urls import path
from hotzone import views

urlpatterns = [
    path('locations', views.list_locations, name='list_locations'),
    path('cases', views.list_cases, name='list_cases'),
    path('viruses', views.list_viruses, name='list_viruses'),
    path('locations/<str:target>', views.show_location_detail, name='show_location_detail'),
    path('cases/<int:target>', views.show_case_detail, name='show_case_detail'),
    path('viruses/<slug:target>', views.show_virus_detail, name='show_virus_detail'),
    path('cases/<int:target>/add_location', views.add_visted_location, name='add_visted_location'),
    path('user_creation', views.user_creation, name='user_creation'),
    path('', views.user_login, name='user_login'),
    path('user_logout', views.user_logout, name='user_logout')
]