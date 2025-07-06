from django.urls import path
from . import views

urlpatterns = [
    path('', views.contact_create, name='contact_create'),
]