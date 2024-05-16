from django.urls import path
from . import views

urlpatterns = [
    path('',views.lossreport, name='lossreport'),
    path('/analyze',views.analyze, name='addlost'),
]


