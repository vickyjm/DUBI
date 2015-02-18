# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Estacionamiento',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Propietario', models.CharField(help_text='Nombre Propio', max_length=50)),
                ('Nombre', models.CharField(max_length=50)),
                ('Direccion', models.TextField(max_length=120)),
                ('Telefono_1', models.CharField(null=True, max_length=30, blank=True)),
                ('Telefono_2', models.CharField(null=True, max_length=30, blank=True)),
                ('Telefono_3', models.CharField(null=True, max_length=30, blank=True)),
                ('Email_1', models.EmailField(null=True, max_length=75, blank=True)),
                ('Email_2', models.EmailField(null=True, max_length=75, blank=True)),
                ('Rif', models.CharField(max_length=12)),
                ('Tarifa', models.CharField(null=True, max_length=50, blank=True)),
                ('Esquema', models.CharField(choices=[('Hora', ' Por hora'), ('Minuto', ' Por minuto'), ('HoraYFraccion', 'Hora y fracción'), ('DifHora', 'Diferenciado por hora')], max_length=20)),
                ('Apertura', models.TimeField(null=True, blank=True)),
                ('Cierre', models.TimeField(null=True, blank=True)),
                ('Reservas_Inicio', models.TimeField(null=True, blank=True)),
                ('Reservas_Cierre', models.TimeField(null=True, blank=True)),
                ('NroPuesto', models.IntegerField(null=True, blank=True)),
                ('Pico_Ini', models.TimeField(null=True, blank=True)),
                ('Pico_Fin', models.TimeField(null=True, blank=True)),
                ('TarifaPico', models.CharField(null=True, max_length=50, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ReservasModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Puesto', models.IntegerField()),
                ('InicioReserva', models.DateTimeField()),
                ('FinalReserva', models.DateTimeField()),
                ('Estacionamiento', models.ForeignKey(to='estacionamientos.Estacionamiento')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
