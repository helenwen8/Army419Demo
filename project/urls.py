"""
URL configuration for finalProject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from eventure import views

urlpatterns = [
    path('', views.home, name='home'),
    path('create_event_info', views.create_event_info, name='create_event_info'),
    path('create_event_attendees/<int:event_id>/', views.create_event_attendees, name='create_event_attendees'),
    path('delete_attendee/<int:attendee_id>/', views.delete_attendee, name='delete_attendee'),
    path('create_event_items/<int:event_id>/', views.create_event_items, name='create_event_items'),
    path('delete_item/<int:item_id>/', views.delete_item, name='delete_item'),
    path('create_event_confirmation/<int:event_id>/', views.create_event_confirmation, name='create_event_confirmation'),
]
