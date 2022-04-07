from django.urls import path
from . import util
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/add", views.add, name="add"),
    path("wiki/<str:name>/edit", views.edit, name="edit"),
    path("wiki/<str:name>",views.wiki, name="wiki"),
]


