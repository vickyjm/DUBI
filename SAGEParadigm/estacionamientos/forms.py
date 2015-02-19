# -*- coding: utf-8 -*-

from django import forms
from django.core.validators import RegexValidator


class EstacionamientoForm(forms.Form):

    phone_validator = RegexValidator(
                            regex = '^((0212)|(0412)|(0416)|(0414)|(0424)|(0426))-?\d{7}',
                            message = 'Debe introducir un formato válido.'
                        )

    # nombre del dueno (no se permiten digitos)
    propietario = forms.CharField(
                    max_length = 50,
                    required = True,
                    label = "Propietario",
                    validators = [
                          RegexValidator(
                                regex = '^[a-zA-ZáéíóúñÑÁÉÍÓÚ ]+$',
                                message = 'Sólo debe contener letras.'
                        )
                    ]
                )

    nombre = forms.CharField(max_length=50,required = True, label = "Nombre")

    direccion = forms.CharField(max_length = 120,required = True)

    telefono_1 = forms.CharField(max_length = 30,required = False, validators = [phone_validator])
    telefono_2 = forms.CharField(max_length = 30,required = False, validators = [phone_validator])
    telefono_3 = forms.CharField(max_length = 30,required = False, validators = [phone_validator])

    email_1 = forms.EmailField(required = False)
    email_2 = forms.EmailField(required = False)

    rif = forms.CharField(
                    max_length = 12,
                    required = True,
                    label = "RIF",
                    validators = [
                          RegexValidator(
                                regex = '^[JVD]-?\d{8}-?\d$',
                                message = 'Introduzca un RIF con un formato válido.'
                        )
                    ]
                )

class EstacionamientoExtendedForm(forms.Form):

    puestos = forms.IntegerField(min_value = 0, label = 'Número de Puestos')

    horarioin = forms.TimeField(required = True, label = 'Hora Apertura')
    horarioout = forms.TimeField(required = True, label = 'Hora Cierre')

    horario_reserin = forms.TimeField(required = True, label = 'Hora Inicio Reserva')
    horario_reserout = forms.TimeField(required = True, label = 'Hora Fin Reserva')
    
    opciones_esquema = (("Hora", " Por hora"), ("Minuto"," Por minuto"), (("HoraFraccion"), ("Hora y fracción")), ("DifHora","Diferenciado por hora"))
    esquema= forms.ChoiceField(required = True, widget = forms.Select(), choices = opciones_esquema)
    tarifa = forms.DecimalField(required = True, max_digits = 9, decimal_places = 2, min_value = 0, label = 'Tarifa')
    
    hora_picoini = forms.TimeField(required = False, label = 'Inicio Hora Pico')
    hora_picofin = forms.TimeField(required = False, label = 'Fin Hora Pico')
    tarifa_pico = forms.DecimalField(required = False, max_digits = 9, decimal_places = 2, min_value = 0, label = 'Tarifa Pico')
    

class EstacionamientoReserva(forms.Form):
    fechaInicio = forms.DateField(label = 'Fecha Inicio Reserva')
    horaInicio = forms.TimeField(label = 'Horario Inicio Reserva')
    fechaFinal = forms.DateField(label = 'Fecha Final Reserva')
    horaFinal = forms.TimeField(label = 'Horario Final Reserva')
