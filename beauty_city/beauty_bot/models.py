from django.db import models


class Services(models.Model):
    name = models.CharField(max_length=50, verbose_name='Услуга')
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Цена'
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'услуга'
        verbose_name_plural = 'Услуги'


class Specialist(models.Model):
    name = models.CharField(max_length=50, verbose_name='Имя мастера')
    service = models.ManyToManyField(
        Services,
        related_name='specialist',
        verbose_name='Услуги'
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'специалист'
        verbose_name_plural = 'Специалист'


class Clients(models.Model):
    name = models.CharField(max_length=50, verbose_name='Имя клиента')
    telegram_username = models.CharField(
        max_length=50,
        verbose_name='Телеграмм'
    )
    phone_number = models.CharField(max_length=50, verbose_name='Телефон')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'клиент'
        verbose_name_plural = 'Имя клиента'


class TimeSlot(models.Model):
    specialist = models.ForeignKey(
        Specialist,
        on_delete=models.CASCADE,
        verbose_name='Специалист'
    )
    date = models.DateField(verbose_name='Дата')
    time = models.TimeField(verbose_name='Время')
    is_booked = models.BooleanField(default=False, verbose_name='Занято')

    def __str__(self):
        return self.name

    class Meta:
        unique_together = ('specialist', 'date', 'time')
        verbose_name = 'слот'
        verbose_name_plural = 'Временной слот'


class Salones(models.Model):
    name = models.CharField(max_length=50, verbose_name='Название')
    Specialist = models.ManyToManyField(
        Specialist,
        verbose_name='Специалисты'
    )
    addres = models.CharField(max_length=100, verbose_name='Адрес', null=True)
    phone_number = models.CharField(max_length=30, verbose_name='Телефон салона', null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'салон'
        verbose_name_plural = 'Салон'


class Schedule(models.Model):
    salone = models.ForeignKey(
        Salones,
        on_delete=models.CASCADE,
        verbose_name='Салон',
        null=True
    )
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

    def __str__(self):
        return f'Запись{self.client} на {self.time_slot} в {self.salone}'

    class Meta:
        unique_together = ('specialist', 'time_slot')
        verbose_name = 'запись'
        verbose_name_plural = 'Запись'
