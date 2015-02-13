# Archivo con funciones de control para SAGE

from decimal import Decimal
import datetime
from math import floor

# Las Tuplas de cada puesto deben tener los horarios de inicio y de cierre para que
# pueda funcionar [(7:00,7:00), (19:00,19:00)]




# Suponiendo que cada estacionamiento tiene una estructura "matricial" lista de listas
# donde si m es una matriz, m[i,j] las i corresponden a los puestos y las j corresponden a tuplas
# con el horario inicio y fin de las reservas
# [[(horaIn,horaOut),(horaIn,horaOut)],[],....]

# chequeo de horarios de extended

# -*- coding: utf-8 -*-

def HorarioEstacionamiento(HoraInicio, HoraFin, ReservaInicio, ReservaFin):

	if HoraInicio >= HoraFin:
		return (False, 'El horario de apertura debe ser menor al horario de cierre')
	if ReservaInicio >= ReservaFin:
		return (False, 'El horario de inicio de reserva debe ser menor al horario de cierre')
	if ReservaInicio < HoraInicio:
		return (False, 'El horario de inicio de reserva debe mayor o igual al horario de apertura del estacionamiento')
	if ReservaInicio > HoraFin:
		return (False, 'El horario de comienzo de reserva debe ser menor al horario de cierre del estacionamiento')
	if ReservaFin < HoraInicio:
		return (False, 'El horario de apertura de estacionamiento debe ser menor al horario de finalizacion de reservas')
	if ReservaFin > HoraFin:
		return (False, 'El horario de cierre de estacionamiento debe ser mayor o igual al horario de finalizacion de reservas')
	return (True, '')


# busca un puesta en el estacionamiento
def buscar(hin, hout, estacionamiento):
	if not isinstance(estacionamiento, list):
		return (-1, -1, False)
	if len(estacionamiento) == 0:
		return (-1, -1, False)
	if not isinstance(hin, datetime.datetime) or not isinstance(hout,datetime.datetime):
		return (-1, -1, False)
	for i in range(len(estacionamiento)):
		posicion = busquedaBin(hin, hout, estacionamiento[i])
		if posicion[1] == True:
			return (i, posicion[0], posicion[1])
	return (-1, -1, False)

def binaria(valor, inicio, fin, lista):
	if inicio == fin:
		return inicio
	centro = (inicio + fin) // 2
	if lista[centro][0] > valor:
		return binaria(valor, inicio, centro, lista)
	if lista[centro][0] < valor:
		return binaria(valor, centro + 1, fin, lista)
	return centro

# Busca en una lista ordenada la posicion en la que una nueva tupla
# puede ser insertado, y ademas devuelve un booleano que dice si la
# tupla puede ser insertada, es decir que sus valores no solapen alguno
# ya existente.
# Precondicion: la lista debe tener ya la mayor y menor posible tupla
def busquedaBin(hin, hout, listaTuplas):
	# ln = len(listaTuplas)
	if not isinstance(listaTuplas, list):
		return (0, False)
	if len(listaTuplas) == 0:
		return (0, True)
	if not isinstance(hin, datetime.datetime) or not isinstance(hout, datetime.datetime):
		return (0, False)
	index = binaria(hin, 0, len(listaTuplas), listaTuplas)
	if index == 0:
		index = index + 1
	if listaTuplas[index][0] >= hout and listaTuplas[index - 1][1] <= hin:
		return (index, True)
	else:
		return (index, False)

# inserta ordenadamente por hora de inicio
def insertarReserva(hin, hout, puesto, listaReserva):
	# no verifica precondicion, se supone que se hace buscar antes para ver si se puede agregar
	if not isinstance(listaReserva, list):
		return None
	if len(listaReserva) == 0:
		return listaReserva
	if not isinstance(hin, datetime.datetime) or not isinstance(hout, datetime.datetime):
		return listaReserva
	tupla = (hin, hout)
	listaReserva.insert(puesto, tupla)
	# estacionamiento[puesto].sort()
	return listaReserva

def reservar(hin, hout, estacionamiento):
	if not isinstance(estacionamiento, list):
		return 1
	if len(estacionamiento) == 0:
		return 1
	if not isinstance(hin, datetime.datetime) or not isinstance(hout, datetime.datetime):
		return 1
	puesto = buscar(hin, hout, estacionamiento)
	if puesto[2] != False:
		estacionamiento[puesto[0]] = insertarReserva(hin, hout, puesto[1], estacionamiento[puesto[0]])
		return estacionamiento
	else:
		return 1
	
def calculoTarifaHora(iniR,finR,tarifa):
	
	assert(finR > iniR)
	assert(tarifa > 0)
	assert(finR >= iniR + datetime.timedelta(hours = 1))
	assert(finR <= iniR + datetime.timedelta(days = 7))
	
	temp1=(finR-iniR).days*24 + (finR - iniR).seconds//3600
	temp2=(finR-iniR).days*24 + (finR - iniR).seconds/3600
	
	if temp1<temp2:
		temp1+=1
		
	return tarifa*temp1

def calculoTarifaMinuto (iniR, finR, tarifa):
	
	assert(finR > iniR)
	assert(tarifa > 0)
	assert(finR >= iniR + datetime.timedelta(hours = 1))
	assert(finR <= iniR + datetime.timedelta(days = 7))
	
	temp1 = (finR-iniR).days*24 + (finR - iniR).seconds//3600
	temp2 = (finR-iniR).days*24 + (finR - iniR).seconds/3600
	minextra = temp2 - temp1
	fraccion = tarifa*minextra
	
	return round(tarifa * temp1 + fraccion,2) 

def calculoTarifaHoraYFraccion(iniR,finR,tarifa):
	
	assert(finR > iniR)
	assert(tarifa > 0)
	assert(finR >= iniR + datetime.timedelta(hours = 1))
	assert(finR <= iniR + datetime.timedelta(days = 7))
	
	fraccion = 0
	diasdif = (finR-iniR).days
	segundosdif =(finR - iniR).seconds
	temp1 = segundosdif//3600
	temp2 = Decimal(segundosdif/3600)
	minextra = round((temp2 - temp1)*60,2)

	if minextra > 30:
		fraccion = tarifa
	elif minextra <= 30 and minextra != 0:
		fraccion = tarifa/2
	
	return round(tarifa*diasdif*24 + tarifa * temp1 + fraccion,2)
	

def validarHorarioReserva(ReservaInicio, ReservaFin, HorarioApertura, HorarioCierre,fechaActual):
	hIni = datetime.time(ReservaInicio.hour,ReservaInicio.minute)
	hFin = datetime.time(ReservaFin.hour,ReservaFin.minute)
	inicioBorde = datetime.time(0,0)
	finBorde = datetime.time(23,59)
	delta = ReservaFin - ReservaInicio
	deltaActual = ReservaInicio - fechaActual
	
	if (delta.days == 0) and (delta.seconds < 3600) :
		return (False, 'El tiempo de reserva debe ser al menos de 1 hora')
	else:
		if (ReservaInicio >= ReservaFin):
			return (False, 'El horario de inicio de reserva debe ser menor que le horario de fin de reserva')
	if hFin > HorarioCierre:
		return (False, 'El horario de inicio de reserva debe estar en un horario valido')
	if hIni < HorarioApertura:
		return (False, 'El horario de cierre de reserva debe estar en un horario valido')
	if ((delta.days == 7) and (delta.seconds > 0)) or (delta.days > 7):
		return (False, 'El tiempo de reserva no puede ser mayor a 7 días')
	elif (delta.days > 0) and ((HorarioApertura != inicioBorde) or (HorarioCierre != finBorde)): # Mayor a un dia y no 24h
		return (False, 'Este estacionamiento no trabaja 24 horas')
	elif (delta.days==7) and (ReservaInicio > fechaActual):
		return (False, 'La reserva debe estar en un intervalo dentro de los próximos 7 días')
	elif (delta.days > 7):
		return (False, 'La reserva no puede ser mayor a 7 días')
	if (deltaActual.days < 0):
		return (False, 'La fecha ingresada para su reserva ya pasó')
	elif (deltaActual.days > 7) or ((deltaActual.days == 7) and (deltaActual.seconds > 0)):
		return (False, 'La reserva puede ser máximo hasta dentro de 7 días')			
	return (True, '')

