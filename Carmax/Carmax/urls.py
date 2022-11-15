"""Carmax URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from core import views

app_name = 'core'

urlpatterns = [
    path('', views.landing, name="landing"),
    path('reservation/', views.new_turn, name="reservation"),
    path('reservation/edit/', views.edit_turn, name="edit-reservation"),
    path("reservation/cancelation/<pk>", views.CancelTurnView.as_view(), name= "cancel-reservation"),
    path('turn_list/', views.TurnListView.as_view(), name="my-turns"),
    path('about/', views.nostros, name="nosotros"),
    path('services/', views.servicios, name="servicios"),
    path('admin/', admin.site.urls),
    # Paths de Auth
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/', include('registration.urls')),
]
