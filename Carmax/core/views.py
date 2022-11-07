from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.models import User
from .models import Turn
from .forms import BookingForm

# Create your views here.
def landing(request):
    return render(request, "core/landing.html")

def nostros(request):
    return render(request, "core/nosotros.html")

def servicios(request):
    return render(request, "core/servicios.html")

def turn_form(request):
    context = {}
    context['form']= BookingForm()
    return render(request, "core/turn_form.html", context)

def new_turn(request):
    turn_form = BookingForm
    form = turn_form(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            data = form.cleaned_data
            available_day_turn = check_day_availability(
                data["date"],
            )
            if available_day_turn is True:
                available_turn = check_availability(
                    data["date"],
                    data["timeblock"],
                )

                if available_turn is True:
                    book_turn(
                    request, 
                    data["date"],
                    data["timeblock"],
                    data["service"],
                    )
                    form.save()
                    return redirect('/')
                else:
                    return HttpResponse("Este horario esta ocupado!")
            else:
                return HttpResponse("No existen turnos disponibles este dia!")
    return render(
        request=request, template_name="landing.html")

def check_day_availability(date):
    turn_list = Turn.objects.filter(date)
    if len(turn_list) == 9: 
        return False
    else:
        return True

def check_availability(date,timeblock):
    turn = Turn.objects.filter(date, timeblock)
    if turn != None:
        return False
    else:
        return True

def book_turn(request, date,timeblock,service_id):
    # Crea un objeto de tipo Booking y lo guarda
    turn = Turn.objects.create(
        date=date,
        timeblock=timeblock,
        service_id=service_id,
        user_id= request.user # Buscar user id de quien mierda esta logueado 
    )
    turn.save()

    return turn