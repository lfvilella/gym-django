from django.contrib import admin
from django.urls import path, include
from .views import treino

urlpatterns = [
    path('treino/', treino, name="treino"),
]
