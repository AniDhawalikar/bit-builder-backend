from django.urls import path
from . import views

urlpatterns = [
    path('get', views.sample_get_api, name='sample api to test'),
]