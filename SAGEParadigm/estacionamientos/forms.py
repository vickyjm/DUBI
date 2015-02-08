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
                    required = True,
                    label = "Propietario",
                    validators = [
                          RegexValidator(
                                regex = '^[a-zA-ZáéíóúñÑÁÉÍÓÚ ]+$',
                                message = 'Sólo debe contener letras.'
                        )
                    ]
                )

    nombre = forms.CharField(required = True, label = "Nombre")

    direccion = forms.CharField(required = True)

    telefono_1 = forms.CharField(required = False, validators = [phone_validator])
    telefono_2 = forms.CharField(required = False, validators = [phone_validator])
    telefono_3 = forms.CharField(required = False, validators = [phone_validator])

    email_1 = forms.EmailField(required = False)
    email_2 = forms.EmailField(required = False)

    rif = forms.CharField(
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

    tarifa_validator = RegexValidator(
                            regex = '^([0-9]+(\.[0-9]+)?)$',
                            message = 'Sólo debe contener dígitos.'
                        )
    
    esquema_validator = RegexValidator(
                            regex='^((Hora)|(hora)|(Minuto)|(minuto))',
                            message='No existe el esquema introducido'
                        )
    

    horarioin = forms.TimeField(required = True, label = 'Hora Apertura')
    horarioout = forms.TimeField(required = True, label = 'Hora Cierre')

    horario_reserin = forms.TimeField(required = True, label = 'Hora Inicio Reserva')
    horario_reserout = forms.TimeField(required = True, label = 'Hora Fin Reserva')
    
    esquema= forms.CharField(required = True, validators = [esquema_validator])

    tarifa = forms.CharField(required = True, validators = [tarifa_validator])

class EstacionamientoReserva(forms.Form):
    inicio = forms.TimeField(label = 'Hora Inicio Reserva')
    final = forms.TimeField(label = 'Hora Final Reserva')
