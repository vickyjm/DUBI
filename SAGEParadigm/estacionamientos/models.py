# -*- coding: utf-8 -*-

from django.core.validators import RegexValidator
from django.db import models
from django.forms import ModelForm
import datetime
from decimal import Decimal
from django.db.models.fields import IntegerField

class Estacionamiento(models.Model):
	# propietario=models.ForeignKey(Propietario)
	Propietario = models.CharField(max_length = 50, help_text = "Nombre Propio")
	Nombre = models.CharField(max_length = 50)
	Direccion = models.TextField(max_length = 120)

	Telefono_1 = models.CharField(blank = True, null = True, max_length = 30)
	Telefono_2 = models.CharField(blank = True, null = True, max_length = 30)
	Telefono_3 = models.CharField(blank = True, null = True, max_length = 30)

	Email_1 = models.EmailField(blank = True, null = True)
	Email_2 = models.EmailField(blank = True, null = True)

	Rif = models.CharField(max_length = 12)

	#Tarifa = models.DecimalField(max_digits = 9, decimal_places = 2,null=True)
	opciones_esquema = (("Hora", " Por hora"), ("Minuto"," Por minuto"), (("HoraFraccion"), ("Hora y fracción")), ("DifHora","Diferenciado por hora"),("DifFin","Diferenciado por fin de semana"))
	Esquema = models.CharField(max_length = 20, choices = opciones_esquema)
	Apertura = models.TimeField(blank = True, null = True)
	Cierre = models.TimeField(blank = True, null = True)
	Reservas_Inicio = models.TimeField(blank = True,null = True)
	Reservas_Cierre = models.TimeField(blank = True, null = True)
	NroPuesto = models.IntegerField(blank = True, null = True)
	#Pico_Ini = models.TimeField(blank = True,null = True)
	#Pico_Fin = models.TimeField(blank = True, null = True)
	#TarifaPico = models.DecimalField(max_digits = 9, decimal_places = 2,null=True)


class ReservasModel(models.Model):
	Estacionamiento = models.ForeignKey(Estacionamiento)
	InicioReserva = models.DateTimeField(blank = True, null = True)
	FinalReserva = models.DateTimeField(blank = True, null = True)

class ReciboPagoModel(models.Model):
	Reserva = models.ForeignKey(ReservasModel)
	numeroRecibo = IntegerField(blank = True, null = True)
	cedula = models.CharField(blank = True, null = True,max_length = 13)
	fechaTransaccion = models.DateTimeField(blank = True, null = True)
	opciones_tarjeta = (('Vista','Vista'), ('Mister','Mister'), ('Xpres','Xpres'))
	TipoTarjeta = models.CharField(max_length = 6, choices = opciones_tarjeta)
	MontoPago = models.DecimalField(max_digits = 12, decimal_places = 2)

class Esquema(models.Model):
	Estacionamiento = models.ForeignKey(Estacionamiento)
	Tarifa = models.DecimalField(max_digits = 9, decimal_places = 2)
	
	# class Meta:
	# abstract = True
	
class Hora(Esquema):
			
	def calcularMonto(self,iniR,finR):
		
		
		temp1=Decimal(str((finR-iniR).days*24 + (finR - iniR).seconds//3600))
		temp2=Decimal(str((finR-iniR).days*24 + (finR - iniR).seconds/3600))
		
		if temp1<temp2:
			temp1+=1
			
		return round(Decimal(str(self.Tarifa*Decimal(temp1))),2)
	
class Minuto(Esquema):
	
	def calcularMonto(self,iniR,finR):
			
		temp1 = Decimal(str((finR-iniR).days*24 + (finR - iniR).seconds//3600))
		temp2 = Decimal(str((finR-iniR).days*24 + (finR - iniR).seconds/3600))
		minextra = temp2 - temp1
		fraccion = self.Tarifa*minextra
		
		return round(Decimal(str(self.Tarifa * temp1 + fraccion)),2)
	
class HoraFraccion(Esquema):
	
	def calcularMonto(self,iniR,finR):
		
		fraccion = 0
		segundosdif =(finR - iniR).total_seconds()
		temp1 = Decimal(str(segundosdif//3600))
		temp2 = Decimal(str(segundosdif/3600))
		minextra = round((temp2 - temp1)*60,2)
	
		if minextra > 30:
			fraccion = Decimal(str(self.Tarifa))
		elif minextra <= 30 and minextra != 0:
			fraccion = Decimal(str(self.Tarifa/2))
		
		return round(Decimal(str(self.Tarifa * temp1 + fraccion)),2)
	
class DifHora(Esquema):
	
	PicoIni=models.TimeField(blank = True,null = True)
	PicoFin=models.TimeField(blank = True,null = True)
	TarifaPico=models.DecimalField(max_digits = 9, decimal_places = 2,null=True)
		
	def calcularMonto(self,iniR,finR):
		
		tempDatetime=iniR
		minpico = 0
		minvalle = 0
		while tempDatetime<finR:
			tempTime=tempDatetime.time()
			if (tempTime>=self.PicoIni and tempTime<self.PicoFin):
				minpico += 1 
			else:
				minvalle += 1
			tempDatetime=tempDatetime+datetime.timedelta(minutes=1)
	
		return round(Decimal(str(Decimal(str(self.Tarifa*minvalle/60)) + Decimal(str(self.TarifaPico*minpico/60)))),2)
	
class DifFin(Esquema):
	
	TarifaFin=models.DecimalField(max_digits = 9, decimal_places = 2,null=True)
	
	def calcularMonto(self,iniR,finR):
		idSabado=5
		idDomingo=6
		tempDatetime=iniR
		tiempoFin=0
		tiempoNoFin=0
		while tempDatetime<finR:	
			tempDatetime2=tempDatetime
			tempDatetime=tempDatetime+datetime.timedelta(hours=1)
			if tempDatetime>finR:
				difMin=(tempDatetime-finR).seconds//60
				if difMin>=1 and difMin<=30:
					if finR.weekday() in range(idSabado,idDomingo+1) and tempDatetime2.weekday() in range(idSabado,idDomingo+1):
						tiempoFin+=1
					elif finR.weekday() not in range(idSabado,idDomingo+1) and tempDatetime2.weekday() not in range(idSabado,idDomingo+1):
						tiempoNoFin+=1
					else:
						if finR.minute==0:
							if tempDatetime2.weekday() in range(idSabado,idDomingo+1):
								tiempoFin+=1
							else:
								tiempoNoFin+=1
						else:
							if self.Tarifa>=self.TarifaFin:
								tiempoNoFin+=1
							else:
								tiempoFin+=1
				elif difMin>30:
					if finR.weekday() in range(idSabado,idDomingo+1) and tempDatetime2.weekday() in range(idSabado,idDomingo+1):
						tiempoFin+=0.5
					elif finR.weekday() not in range(idSabado,idDomingo+1) and tempDatetime2.weekday() not in range(idSabado,idDomingo+1):
						tiempoNoFin+=0.5
					else:
						if finR.minute==0:
							if tempDatetime2.weekday() in range(idSabado,idDomingo+1):
								tiempoFin+=0.5
							else:
								tiempoNoFin+=0.5
						else:
							if self.Tarifa>=self.TarifaFin:
								tiempoNoFin+=0.5
							else:
								tiempoFin+=0.5
			else:				
				if tempDatetime.weekday() in range(idSabado,idDomingo+1) and tempDatetime2.weekday() in range(idSabado,idDomingo+1):
					tiempoFin+=1
				elif tempDatetime.weekday() not in range(idSabado,idDomingo+1) and tempDatetime2.weekday() not in range(idSabado,idDomingo+1):
					tiempoNoFin+=1
				else:
					if tempDatetime.minute==0:
						if tempDatetime2.weekday() in range(idSabado,idDomingo+1):
							tiempoFin+=1
						else:
							tiempoNoFin+=1
					else:
						if self.Tarifa>=self.TarifaFin:
							tiempoNoFin+=1
						else:
							tiempoFin+=1					
		return round(Decimal(str(self.Tarifa*Decimal(tiempoNoFin) + self.TarifaFin*Decimal(tiempoFin))),2)		
