from django import forms
from datetime import date
from .models import Turn


class DateInput(forms.DateInput):
    input_type = 'date'

class BookingForm(forms.ModelForm):
    TIME_LIST = (
        (1, '09:00 - 10:00'),
        (2, '10:00 - 11:00'),
        (3, '11:00 - 12:00'),
        (4, '12:00 - 13:00'),
        (5, '13:00 - 14:00'),
        (6, '14:00 - 15:00'),
        (7, '15:00 - 16:00'),
        (8, '16:00 - 17:00'),
        (9, '17:00 - 18:00'),
    )
    date = forms.DateField(widget=DateInput)
    timeblock = forms.ChoiceField(choices=TIME_LIST)

    class Meta:
        model = Turn
        fields = ('service','date','timeblock')


    def clean_date(self):
        day = self.cleaned_data['date']

        if day <= date.today():
            raise forms.ValidationError('No puede elegir un día que ya pasó.', code='invalid')
        if day.isoweekday() in (0, 5):
            raise forms.ValidationError('Nuestro horario de trabajo es de lunes a viernes de 09:00 a 18:00 horas.', code='invalid')

        return day