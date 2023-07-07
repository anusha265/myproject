# pdfreorder/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.reorder_pdf, name='reorder_pdf'),
]