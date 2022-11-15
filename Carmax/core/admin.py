from django.contrib import admin
from .models import Turn, Service

# Register your models here.
@admin.register(Turn)
class TurnAdmin(admin.ModelAdmin):
    ordering = ('user','service','date', 'timeblock')
    search_fields = ('date', 'timeblock')
    list_filter = ('date', 'timeblock')
    list_per_page = 15

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    ordering = ('service',)