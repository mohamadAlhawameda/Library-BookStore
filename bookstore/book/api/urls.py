from django.urls import path
from . import views

urlpatterns = [
    path('',  views.getRoutes),
    path('books/', views.getBook),
    path('books/<str:pk>/', views.getBook),
]
