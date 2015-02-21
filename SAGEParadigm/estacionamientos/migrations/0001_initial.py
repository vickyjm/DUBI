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
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('Tarifa', models.DecimalField(max_digits=9, decimal_places=2)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='DifHora',
            fields=[
                ('esquema_ptr', models.OneToOneField(parent_link=True, to='estacionamientos.Esquema', primary_key=True, auto_created=True, serialize=False)),
                ('PicoIni', models.TimeField(blank=True, null=True)),
                ('PicoFin', models.TimeField(blank=True, null=True)),
                ('TarifaPico', models.DecimalField(max_digits=9, decimal_places=2, null=True)),
            ],
            options={
            },
            bases=('estacionamientos.esquema',),
        ),
        migrations.CreateModel(
            name='Estacionamiento',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('Propietario', models.CharField(max_length=50, help_text='Nombre Propio')),
                ('Nombre', models.CharField(max_length=50)),
                ('Direccion', models.TextField(max_length=120)),
                ('Telefono_1', models.CharField(max_length=30, blank=True, null=True)),
                ('Telefono_2', models.CharField(max_length=30, blank=True, null=True)),
                ('Telefono_3', models.CharField(max_length=30, blank=True, null=True)),
                ('Email_1', models.EmailField(max_length=75, blank=True, null=True)),
                ('Email_2', models.EmailField(max_length=75, blank=True, null=True)),
                ('Rif', models.CharField(max_length=12)),
                ('Esquema', models.CharField(max_length=20, choices=[('Hora', ' Por hora'), ('Minuto', ' Por minuto'), ('HoraFraccion', 'Hora y fracción'), ('DifHora', 'Diferenciado por hora')])),
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
        migrations.CreateModel(
            name='Hora',
            fields=[
                ('esquema_ptr', models.OneToOneField(parent_link=True, to='estacionamientos.Esquema', primary_key=True, auto_created=True, serialize=False)),
            ],
            options={
            },
            bases=('estacionamientos.esquema',),
        ),
        migrations.CreateModel(
            name='HoraFraccion',
            fields=[
                ('esquema_ptr', models.OneToOneField(parent_link=True, to='estacionamientos.Esquema', primary_key=True, auto_created=True, serialize=False)),
            ],
            options={
            },
            bases=('estacionamientos.esquema',),
        ),
        migrations.CreateModel(
            name='Minuto',
            fields=[
                ('esquema_ptr', models.OneToOneField(parent_link=True, to='estacionamientos.Esquema', primary_key=True, auto_created=True, serialize=False)),
            ],
            options={
            },
            bases=('estacionamientos.esquema',),
        ),
        migrations.CreateModel(
            name='PagoReservaModel',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('TipoTarjeta', models.CharField(max_length=6, choices=[('Vista', 'Vista'), ('Mister', 'Mister'), ('Xpres', 'Xpres')])),
                ('NumTarjeta', models.CharField(max_length=19)),
                ('MontoPago', models.DecimalField(max_digits=12, decimal_places=2)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ReservasModel',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('InicioReserva', models.DateTimeField()),
                ('FinalReserva', models.DateTimeField()),
                ('Estacionamiento', models.ForeignKey(to='estacionamientos.Estacionamiento')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='pagoreservamodel',
            name='Reserva',
            field=models.ForeignKey(to='estacionamientos.ReservasModel'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='esquema',
            name='Estacionamiento',
            field=models.ForeignKey(to='estacionamientos.Estacionamiento'),
            preserve_default=True,
        ),
    ]
