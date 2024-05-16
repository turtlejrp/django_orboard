from django.urls import path
from . import views

urlpatterns = [
    path('',views.orboard, name='orboardday'),
]
