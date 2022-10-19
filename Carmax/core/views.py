from django.shortcuts import render

# Create your views here.
def landing(request):
    return render(request, "core/landing.html")

def nostros(request):
    return render(request, "core/nosotros.html")

def servicios(request):
    return render(request, "core/servicios.html")

def registracion(request):
    return render(request, "core/registration.html")

def login(request):
    return render(request, "core/login.html")