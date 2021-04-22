from django.urls import path     
from . import views


urlpatterns = [
    path('', views.index),
    path('main', views.main),
    # path('users/create', views.create_user),
    # path('users/login', views.login),
    # path('logout', views.logout),
    path('add_therapist', views.add_therapist),
    path('therapist/added', views.create_therapist),
    path('add_client', views.add_client),   
    path('client/added', views.create_client),
    # path('about_therapist', views.about_therapist),
    path('therapists/<int:therapist_id>/edit_therapist', views.edit_therapist), 
    path('therapists/<int:therapist_id>/edit', views.edit_therapist), 
    path('therapists/<int:therapist_id>/update', views.update_therapist),
    path('client/<int:client_id>/edit', views.edit_client),    
    path('client/<int:client_id>/update', views.update_client),
    path('therapists/<int:therapist_id>/about', views.show_therapist),
    path('client/<int:client_id>/about', views.show_client),
    path('therapists/<int:therapist_id>/delete', views.delete_therapist),
    path('client/<int:client_id>/delete', views.delete_client),

]
