# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Esquema',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('Tarifa', models.DecimalField(max_digits=9, decimal_places=2)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='DifHora',
            fields=[
                ('esquema_ptr', models.OneToOneField(serialize=False, auto_created=True, to='estacionamientos.Esquema', primary_key=True)),
                ('PicoIni', models.TimeField(blank=True, null=True)),
                ('PicoFin', models.TimeField(blank=True, null=True)),
                ('TarifaPico', models.DecimalField(max_digits=9, null=True, decimal_places=2)),
            ],
            options={
            },
            bases=('estacionamientos.esquema',),
        ),
        migrations.CreateModel(
            name='Estacionamiento',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('Propietario', models.CharField(help_text='Nombre Propio', max_length=50)),
                ('Nombre', models.CharField(max_length=50)),
                ('Direccion', models.TextField(max_length=120)),
                ('Telefono_1', models.CharField(blank=True, null=True, max_length=30)),
                ('Telefono_2', models.CharField(blank=True, null=True, max_length=30)),
                ('Telefono_3', models.CharField(blank=True, null=True, max_length=30)),
                ('Email_1', models.EmailField(blank=True, null=True, max_length=75)),
                ('Email_2', models.EmailField(blank=True, null=True, max_length=75)),
                ('Rif', models.CharField(max_length=12)),
                ('Esquema', models.CharField(choices=[('Hora', ' Por hora'), ('Minuto', ' Por minuto'), ('HoraFraccion', 'Hora y fracción'), ('DifHora', 'Diferenciado por hora')], max_length=20)),
                ('Apertura', models.TimeField(blank=True, null=True)),
                ('Cierre', models.TimeField(blank=True, null=True)),
                ('Reservas_Inicio', models.TimeField(blank=True, null=True)),
                ('Reservas_Cierre', models.TimeField(blank=True, null=True)),
                ('NroPuesto', models.IntegerField(blank=True, null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='esquema',
            name='Estacionamiento',
            field=models.ForeignKey(to='estacionamientos.Estacionamiento'),
            preserve_default=True,
        ),
        migrations.CreateModel(
            name='Hora',
            fields=[
                ('esquema_ptr', models.OneToOneField(serialize=False, auto_created=True, to='estacionamientos.Esquema', primary_key=True)),
            ],
            options={
            },
            bases=('estacionamientos.esquema',),
        ),
        migrations.CreateModel(
            name='HoraFraccion',
            fields=[
                ('esquema_ptr', models.OneToOneField(serialize=False, auto_created=True, to='estacionamientos.Esquema', primary_key=True)),
            ],
            options={
            },
            bases=('estacionamientos.esquema',),
        ),
        migrations.CreateModel(
            name='Minuto',
            fields=[
                ('esquema_ptr', models.OneToOneField(serialize=False, auto_created=True, to='estacionamientos.Esquema', primary_key=True)),
            ],
            options={
            },
            bases=('estacionamientos.esquema',),
        ),
        migrations.CreateModel(
            name='ReservasModel',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
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
