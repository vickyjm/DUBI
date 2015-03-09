# -*- coding: utf-8 -*-

from django import forms
from django.core.validators import RegexValidator

# Form para la creación de un estacionamiento

class EstacionamientoForm(forms.Form):

    phone_validator = RegexValidator(
                            regex = '^((0212)|(0412)|(0416)|(0414)|(0424)|(0426))-\d{7}',
                            message = 'Debe introducir un formato válido.'
                        )
    
    # Para el nombre del dueño no se permiten dígitos
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

    direccion = forms.CharField(max_length = 120,required = True, label = "Dirección")

    telefono_1 = forms.CharField(max_length = 30,required = False, validators = [phone_validator])
    telefono_2 = forms.CharField(max_length = 30,required = False, validators = [phone_validator])
    telefono_3 = forms.CharField(max_length = 30,required = False, validators = [phone_validator])

    email_1 = forms.EmailField(required = False)
    email_2 = forms.EmailField(required = False)

    rif = forms.CharField(
                    max_length = 13,
                    required = True,
                    label = "RIF",
                    validators = [
                          RegexValidator(
                                regex = '^[JVD]-\d{8}-\d$',
                                message = 'Introduzca un RIF con un formato válido.'
                        )
                    ]
                )

# Form para la parametrización de un estacionamiento

class EstacionamientoExtendedForm(forms.Form):

    puestos = forms.IntegerField(min_value = 0, label = 'Número de Puestos')

    horarioin = forms.TimeField(required = True, label = 'Hora de Apertura')
    horarioout = forms.TimeField(required = True, label = 'Hora de Cierre')

# Form para las opciones de esquemas y sus respectivos parámetros    
    
class EsquemaForm(forms.Form):
   
    opciones_esquema = (("Hora", " Por hora"), ("Minuto"," Por minuto"), (("HoraFraccion"), \
                                ("Hora y fracción")), ("DifHora","Diferenciado por hora"), \
                                ("DifFin","Diferenciado por fin de semana"))
    
    esquema= forms.ChoiceField(required = True, widget = forms.Select(), \
                               choices = opciones_esquema, label = 'Esquema')
    tarifa = forms.DecimalField(required = True, max_digits = 9, decimal_places = 2,\
                                                        min_value = 0, label = 'Tarifa')
    
    tarifa_fin = forms.DecimalField(required = False, max_digits = 9, decimal_places = 2, \
                                            min_value = 0, label = 'Tarifa de Fin de Semana')
    
    hora_picoini = forms.TimeField(required = False, label = 'Inicio de Horario Pico')
    hora_picofin = forms.TimeField(required = False, label = 'Fin de Horario Pico')
    tarifa_pico = forms.DecimalField(required = False, max_digits = 9, decimal_places = 2, \
                                            min_value = 0.01, label = 'Tarifa de Horario Pico')
    
# Form para la reserva en un estacionamiento

class EstacionamientoReserva(forms.Form):
    
    fechaInicio = forms.DateField(label = 'Fecha Inicio Reserva')
    horaInicio = forms.TimeField(label = 'Hora Inicio Reserva')
    
    fechaFinal = forms.DateField(label = 'Fecha Final Reserva')
    horaFinal = forms.TimeField(label = 'Hora Final Reserva')
    
# Form para el pago de una reserva (recibo de pago)    
    
class PagoReserva(forms.Form):
    
    nombre = forms.CharField(
                    max_length = 100,
                    required = True,
                    label = "Nombre",
                    validators = [
                          RegexValidator(
                                regex = '^[a-zA-ZáéíóúñÑÁÉÍÓÚüÜ][a-zA-ZáéíóúñÑÁÉÍÓÚüÜ ]*$',
                                message = 'Sólo debe contener letras.'
                        )
                    ]
                )
    
    apellidos = forms.CharField(
                    max_length = 100,
                    required = True,
                    label = "Apellidos",
                    validators = [
                          RegexValidator(
                                regex = '^[a-zA-ZáéíóúñÑÁÉÍÓÚüÜ][a-zA-ZáéíóúñÑÁÉÍÓÚüÜ ]*$',
                                message = 'Sólo debe contener letras.'
                        )
                    ]
                ) 
    
    nacionalidad = forms.ChoiceField(required = True, widget = forms.Select(), \
                                     choices = (("V-","V-"),("E-","E-")))
    
    cedula = forms.CharField(
                    max_length = 11,
                    required = True,
                    label = "Cédula de Identidad",
                    validators = [
                        RegexValidator(
                            regex = '^([1-9][0-9]{0,3})(\.?[0-9]{3}){0,2}$',
                            message = 'Formato erróneo'
                        )
                    ]
            )
    
    numTarjeta_validator = RegexValidator(
                                regex = '^\d{4}-?\d{4}-?\d{4}-?\d{4}$',
                                message = 'Formato erróneo'          
                                          )
    
    tipoTarjeta = forms.ChoiceField(required = True, widget = forms.Select(), \
                                    choices = (("Vista","Vista"),("Mister","Mister"),("Xpres","Xpres")))
    
    numTarjeta = forms.CharField(required = True,label = "Número de Tarjeta",\
                                 validators = [numTarjeta_validator])                                
