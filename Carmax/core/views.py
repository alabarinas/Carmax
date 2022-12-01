from django.shortcuts import render, HttpResponse, redirect
from datetime import date
from django.views.generic import ListView, DeleteView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect
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
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse_lazy('login'))
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
                    data["service"].id,
                    request.user.id,
                    )
                    return redirect('/')
                else:
                    #return HttpResponse("Este horario esta ocupado!")
                    return HttpResponseRedirect(reverse_lazy('reservation') + '?invalid-time')
            else:
                #return HttpResponse("No existen turnos disponibles este dia!")
                return HttpResponseRedirect(reverse_lazy('reservation') + '?invalid-date')
    return render(request=request, template_name="core/turn_form.html", context={"form": form},)

def check_day_availability(date):
    
    turn_list = Turn.objects.all()
    count=0

    for t in turn_list:
        if t.date==date:
            count=count+1
            
    if count == 9:  
        return False
    else:
        return True
    
    
    

def check_availability(date, timeblock):
    timeblock = int(timeblock)
    turns = Turn.objects.all()
    new_turn= None
    
    for t in turns:
        if t.date==date and t.timeblock == timeblock:
            new_turn = t
    
    if new_turn != None:
        return False
    else:
        return True

def book_turn(request, date, timeblock, serviceId, userId):
    # Crea un objeto de tipo Turn y lo guarda
    turn = Turn.objects.create(
        date=date,
        timeblock=timeblock,
        service_id=serviceId,
        user_id= userId
    )
    turn.save()

    return turn

@method_decorator(login_required, name='dispatch')
class TurnListView(ListView):
    model = Turn
    template_name = "core/my_turns.html"

    def get_queryset(self, *args, **kwargs):
        if self.request.user.is_staff:
            turn_list = Turn.objects.filter(date__gte= date.today()).order_by('date','timeblock')
            return turn_list
        else:
            turn_list = Turn.objects.filter(user=self.request.user, date__gte= date.today()).order_by('date','timeblock')
            return turn_list

@method_decorator(login_required, name='dispatch')
class CancelTurnView(DeleteView):
    model = Turn
    template_name = "core/cancel_turn_view.html"
    success_url = reverse_lazy("my-turns")
            
