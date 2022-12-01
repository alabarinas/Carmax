from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse


# Create your models here.
class Service(models.Model):
    SERVICE_CATEGORIES = (
        ("Revisión de bateria"),
        ("Mantenimiento general"),
        ("Reparación de motor"),
        ("Cambio de aceite"),
    )

    service = models.CharField(max_length=200 ,verbose_name ="name")

    def __str__(self):
        return str(self.service) 

class Turn(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now,help_text="DD-MM-AAAA")

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

    timeblock = models.IntegerField(blank=True, null=True, choices=TIME_LIST, default="Elija el horario")

     
    class Meta:
        unique_together = ('user','date', 'timeblock')
    

    def __str__(self):
        return '{} {} {}. Cliente: {}'.format(self.date, self.service, self.get_timeblock_display(), self.user.email)

    @property
    def time(self):
        return self.TIME_LIST[self.timeblock][1]

    def get_cancel_turn_url(self):
        return reverse(
            "cancel-reservation",
            args=[
                self.pk,
            ],
        )