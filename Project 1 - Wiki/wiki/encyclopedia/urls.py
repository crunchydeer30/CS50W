from django.urls import path
from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:entry>", views.view_entry, name="entry_view"),
    path("add/", views.new_entry, name="new_entry"),
    path("search/", views.search, name="search"),
    path("random/", views.random_page, name="random"),
    path("wiki/<str:entry>/edit/", views.edit, name="edit"),
    path("wiki/<str:entry>/remove/", views.remove, name="remove")    
]

