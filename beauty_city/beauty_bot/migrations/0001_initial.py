# Generated by Django 4.2.17 on 2024-12-17 17:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Clients',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Имя клиента')),
                ('telegram_username', models.CharField(max_length=50, verbose_name='Телеграмм')),
                ('phone_number', models.CharField(max_length=50, verbose_name='Телефон')),
            ],
        ),
        migrations.CreateModel(
            name='Services',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Услуга')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Цена')),
            ],
        ),
        migrations.CreateModel(
            name='Specialist',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Имя мастера')),
                ('service', models.ManyToManyField(related_name='specialist', to='beauty_bot.services', verbose_name='Услуги')),
            ],
        ),
        migrations.CreateModel(
            name='TimeSlot',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(verbose_name='Дата')),
                ('time', models.TimeField(verbose_name='Время')),
                ('is_booked', models.BooleanField(default=False, verbose_name='Занято')),
                ('specialist', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='beauty_bot.specialist', verbose_name='Специалист')),
            ],
            options={
                'unique_together': {('specialist', 'date', 'time')},
            },
        ),
        migrations.CreateModel(
            name='Schedule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='beauty_bot.clients', verbose_name='Клиент')),
                ('service', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='beauty_bot.services', verbose_name='Услуга')),
                ('specialist', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='beauty_bot.specialist', verbose_name='Специалист')),
                ('time_slot', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='beauty_bot.timeslot', verbose_name='Временной слот')),
            ],
            options={
                'unique_together': {('specialist', 'time_slot')},
            },
        ),
    ]