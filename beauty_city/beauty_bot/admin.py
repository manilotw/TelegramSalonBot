from django.contrib import admin
from .models import Services, Specialist, Clients, TimeSlot, Schedule, Salones


class ServicesAdmin(admin.ModelAdmin):
    list_display = ('name', 'price')


class SpecialistAdmin(admin.ModelAdmin):
    list_display = ('name',)


class ClientsAdmin(admin.ModelAdmin):
    list_display = ('name', 'telegram_username', 'phone_number')
    search_fields = ('name', 'telegram_username', 'phone_number')


class TimeSlotAdmin(admin.ModelAdmin):
    list_display = ('specialist', 'date', 'time', 'is_booked')


class ScheduleAdmin(admin.ModelAdmin):
    list_display = ('specialist', 'client', 'service', 'time_slot')


class SalonesAdmin(admin.ModelAdmin):
    list_display = ('name', 'addres', 'phone_number')


admin.site.register(Services, ServicesAdmin)
admin.site.register(Specialist, SpecialistAdmin)
admin.site.register(Clients, ClientsAdmin)
admin.site.register(TimeSlot, TimeSlotAdmin)
admin.site.register(Schedule, ScheduleAdmin)
admin.site.register(Salones, SalonesAdmin)
