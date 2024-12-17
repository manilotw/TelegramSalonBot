from django.db import models


class Services(models.Model):
    name = models.CharField(max_length=50, verbose_name='Услуга')
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Цена'
    )


class Specialist(models.Model):
    name = models.CharField(max_length=50, verbose_name='Имя мастера')
    service = models.ManyToManyField(
        Services,
        related_name='specialist',
        verbose_name='Услуги'
    )


class Clients(models.Model):
    name = models.CharField(max_length=50, verbose_name='Имя клиента')
    telegram_username = models.CharField(
        max_length=50,
        verbose_name='Телеграмм'
    )
    phone_number = models.CharField(max_length=50, verbose_name='Телефон')


class TimeSlot(models.Model):
    specialist = models.ForeignKey(
        Specialist,
        on_delete=models.CASCADE,
        verbose_name='Специалист'
    )
    date = models.DateField(verbose_name='Дата')
    time = models.TimeField(verbose_name='Время')
    is_booked = models.BooleanField(default=False, verbose_name='Занято')

    class Meta:
        unique_together = ('specialist', 'date', 'time')


class Schedule(models.Model):
    specialist = models.ForeignKey(
        Specialist,
        on_delete=models.CASCADE,
        verbose_name='Специалист'
    )
    client = models.ForeignKey(
        Clients,
        on_delete=models.CASCADE,
        verbose_name='Клиент'
    )
    service = models.ForeignKey(
        Services,
        on_delete=models.CASCADE,
        verbose_name='Услуга'
    )
    time_slot = models.ForeignKey(
        TimeSlot,
        on_delete=models.CASCADE,
        verbose_name='Временной слот'
    )

    class Meta:
        unique_together = ('specialist', 'time_slot')
