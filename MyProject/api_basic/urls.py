from django.contrib import admin
from django.urls import path
from .views import sign,show,add,delete
urlpatterns = [
    path('sign', sign),
    path('show', show),
    path('add', add),
    path('delete', delete),
]