# -*- coding: utf-8 -*-

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
def buscar(hin, hout, estacionamiento,puestos):
    if not isinstance(estacionamiento, list):
        return (-1, -1, False)
    if len(estacionamiento) == 0:
        return (-1, -1, False)
    if not isinstance(hin, datetime.datetime) or not isinstance(hout, datetime.datetime):
        return (-1, -1, False)
    for i in range(len(estacionamiento)):
        exito,reservas = reservar(hin, hout, estacionamiento,puestos)
        if exito == True:
            return (i, 1, exito)
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
#def busquedaBin(hin, hout, listaTuplas):
    # ln = len(listaTuplas)
#   if not isinstance(listaTuplas, list):
#       return (0, False)
#   if len(listaTuplas) == 0:
#       return (0, True)
#   if not isinstance(hin, datetime.datetime) or not isinstance(hout, datetime.datetime):
#       return (0, False)
#   index = binaria(hin, 0, len(listaTuplas), listaTuplas)
#   if index == 0:
#       index = index + 1
#   if listaTuplas[index][0] >= hout and listaTuplas[index - 1][1] <= hin:
#       return (index, True)
#   else:
#       return (index, False)

def marzullo(tabla,puestos):
    best = 0
    cnt = 0
    listaOut = []
    beststart = 0
    bestend = 0
        
    for i in range(len(tabla)-1) :
        if (tabla[i][1] == -1) : 
            cnt = cnt+1
        else :
            cnt = cnt-1
        
        if (cnt > best) :
            best = cnt
            beststart=tabla[i][0]
            bestend = tabla[i+1][0]
        elif (best == cnt) and (best == puestos) :
            if (listaOut.count([tabla[i][0],tabla[i+1][0]]) == 0) and (tabla[i][0] != tabla[i+1][0]) :
                listaOut.append([tabla[i][0],tabla[i+1][0]])
        
    listaOut.append([beststart,bestend])
    listaOut.append([best,0])
    return listaOut

def reservar(horaIni,horaFin,tabla,puestos) :
        
        # Verificacion de entrada
    if ((horaIni.hour < 6) or (horaFin.hour > 18)) or (horaFin.hour-horaIni.hour <= 0) or ((horaFin.hour == 18) and (horaFin.minute != 0)):
        return False,tabla  
    if len(tabla) < 1:
        tabla.append([horaIni,-1])
        tabla.append([horaFin,1])
        return True,tabla


    reservaOrdenada = tabla
    #reservaOrdenada.sort()
    #reservaOrdenada.sort(key=lambda k: (k[0],-k[1]), reverse=True)
    i = 0
    reservaIni = []
    reservaFin = []
    while i < len(reservaOrdenada):
        if reservaOrdenada[i][1] == -1:
            reservaIni.append(reservaOrdenada[i][0])
        else:
            reservaFin.append(reservaOrdenada[i][0])
        i+=1
    reservaIni.sort()
    reservaFin.sort()
    i = 0
    while i < len(reservaIni):
        reservaIni[i] = [reservaIni[i],-1]
        reservaFin[i] = [reservaFin[i],1]
        i+=1

    reservaOrdenada = reservaIni + reservaFin
         
    listaIntervalo = marzullo(reservaOrdenada,puestos) # Devuelve la lista de todos los intervalos maximos
    best = listaIntervalo[len(listaIntervalo)-1][0] # Aqui esta el best 
        
    if (best == puestos):
        i = 0
        while (i<len(listaIntervalo)-1):
            print listaIntervalo
            if (((listaIntervalo[i][0] <= horaIni < listaIntervalo[i][1]) or (listaIntervalo[i][0] <  horaFin <= listaIntervalo[i][1])) or ((horaIni < listaIntervalo[i][0]) and (horaFin > listaIntervalo[i][1]))):
                return False,tabla
            i = i + 1
    tabla.append([horaIni,-1]) # Se agregan las horas aceptadas a la lista de las reservas
    tabla.append([horaFin,1])
    return True,tabla

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

#def reservar(hin, hout, estacionamiento):
#   if not isinstance(estacionamiento, list):
#       return 1
#   if len(estacionamiento) == 0:
#       return 1
#   if not isinstance(hin, datetime.datetime) or not isinstance(hout, datetime.datetime):
#       return 1
#   puesto = buscar(hin, hout, estacionamiento)
#   if puesto[2] != False:
#       estacionamiento[puesto[0]] = insertarReserva(hin, hout, puesto[1], estacionamiento[puesto[0]])
#       return estacionamiento
#   else:
#       return 1
    
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

