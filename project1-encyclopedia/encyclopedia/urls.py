from django.urls import path
from django.urls.conf import re_path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:entry>", views.wiki, name="wiki"),
    path("search", views.search, name="search"),
    path("newpage", views.newpage, name="newpage"),
    path("wiki/<str:entry>/edit", views.edit, name="edit"),
    path("random", views.randompage, name="randompage")
]
