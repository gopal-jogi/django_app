from django.urls import path
from .views import *

urlpatterns = [
    path('magika/', MagikaApi, name='magika'),
]