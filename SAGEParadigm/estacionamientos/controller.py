# -*- coding: utf-8 -*-

# Archivo con funciones de control para SAGE

from decimal import Decimal
import datetime
from estacionamientos.models import ReciboPagoModel
from estacionamientos.models import ReservasModel

import plotly.plotly as py
from plotly.graph_objs import *
py.sign_in('monica.figuera', 'z6pyvhq79s')


# Función para verificar el horario de funcionamiento de un estacionamiento

def HorarioEstacionamiento(HoraInicio, HoraFin):
	if HoraInicio >= HoraFin:
		return (False, 'El horario de apertura debe ser menor al horario de cierre')
	return (True, '')

# Algoritmo que determina los intervalos de tiempo con mayor ocupación de puestos en un estacionamiento

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

# Función que permite verificar la disponibilidad de un puesto en un estacionamiento para
# una reserva determinada usando el algoritmo de Marzullo

def reservar(horaIni,horaFin,tabla,puestos) :
	
    reservaOrdenada = tabla

    reservaOrdenada.sort()
    reservaOrdenada.sort(key=lambda k: (k[0],-k[1]))
    
    listaIntervalo = marzullo(reservaOrdenada,puestos) # Devuelve la lista de todos los intervalos maximos
    best = listaIntervalo[len(listaIntervalo)-1][0] 
        
    if (best == puestos):
        i = 0
        while (i<len(listaIntervalo)-1):
            if (((listaIntervalo[i][0] <= horaIni < listaIntervalo[i][1]) or (listaIntervalo[i][0] <  horaFin <= listaIntervalo[i][1])) or ((horaIni < listaIntervalo[i][0]) and (horaFin > listaIntervalo[i][1]))):
                return False
            i = i + 1
    return True

# Devuelve una matriz con el porcentaje de ocupación por horas del día actual
# y de los próximos 7 días válidos de reserva a partir de él

def calcularTasaReservaHoras(tabla,Apertura, Cierre,NroPuesto,DiaActual):
    estadistica = []
    horas = []

    if Cierre.hour == 23 and Cierre.minute > 0:
        longFin = 24
    else:
        longFin = Cierre.hour
    for i in range(Apertura.hour,longFin):
        horas.append(i)    
    aux = []
    for dia in range(0,8):
        for i in range(Apertura.hour,longFin):
            aux.append(0)
        estadistica.append(aux)
        aux = []
    entrar = False
    for i in range(len(tabla)):	
        if (tabla[i][1] == 1) & (tabla[i-1][0] >= DiaActual):
            diaEstad = (tabla[i-1][0] - DiaActual).days
            if tabla[i-1][0].hour*3600 + tabla[i-1][0].minute*60 + tabla[i-1][0].second < DiaActual.hour*3600+DiaActual.minute*60+DiaActual.second:
                diaEstad += 1
            rango = (tabla[i][0]-tabla[i-1][0]).days+1 # Cantidad de días que abarca la reserva
            if (tabla[i][0].hour*3600 + tabla[i][0].minute*60 + tabla[i][0].second) < (tabla[i-1][0].hour*3600 + tabla[i-1][0].minute*60 + tabla[i-1][0].second):
                rango += 1

            for dia in range(0,rango):
                # Cuando hay una reserva de más de dos días,
                # se llenan directamente los puestos de los días intermedidos
                if dia != 0 and dia != rango-1:
                    for hora in range(len(estadistica[dia])):
                        porcentaje = 100/NroPuesto
                        estadistica[diaEstad][hora] += Decimal('%.1f' % porcentaje)
                else:
                    # Se asignan los valores iniciales para hacer el cálculo de los porcentajes
                    if dia == 0:		
                        HoraIni = tabla[i-1][0].hour
                        MinIni = tabla[i-1][0].minute
                        if rango > 1:					     
                            HoraFin = 24
                            MinFin = 0
                        else:
                            HoraFin = tabla[i][0].hour
                            MinFin = tabla[i][0].minute
                        entrar = True
                    elif dia == rango-1: 					
                        HoraIni = 0
                        MinIni = 0
                        HoraFin = tabla[i][0].hour
                        MinFin = tabla[i][0].minute                    
                    # Se llenan las horas de reserva para el día "DiaEstad"    
                    for j in range(len(horas)):
                        if (HoraIni == horas[j]):
                            while ( (HoraFin*60+MinFin) - (HoraIni*60+MinIni) > 0 ):
                                minutosDif = (HoraFin*60+MinFin) - (HoraIni*60+MinIni)
                                if minutosDif >= 60:
                                    if (MinIni != 0) and (entrar):
                                        TiempoOcup = 60 - MinIni
                                        MinFin -= 60 - MinIni
                                        entrar = False
                                    else:
                                        TiempoOcup = 60
                                        HoraFin -= 1
                                else:
                                    TiempoOcup = minutosDif
                                    HoraFin -= 1
                                porcentaje = (TiempoOcup*100/60)/NroPuesto
                                estadistica[diaEstad][j] += Decimal('%.1f' % porcentaje)
                                j += 1
                diaEstad += 1
    return estadistica

# Función para validar que la reserva de puesto que se desea hacer es válida (está dentro del horario de
# funcionamiento del estacionamiento, la reserva es de al menos un día, está dentro de los próximos
# 7 días, entre otros requerimientos)

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
            return (False, 'La hora de inicio de la reserva debe ser menor que la hora de fin de la reserva')
    if hFin > HorarioCierre:
        return (False, 'La hora de fin de la reserva debe estar en un horario valido')
    if hIni < HorarioApertura:
        return (False, 'La hora de inicio de la reserva debe estar en un horario valido')
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

# Función para verificar que los parámetros del esquema Diferenciado Por Hora son correctos

def validarPicos(HorarioApertura,HorarioCierre,horaPicoIni,horaPicoFin,tarifa,tarifaPico):
	if horaPicoIni is None or horaPicoFin is None or tarifaPico is None:
		return (False,'Los campos Picos son obligatorios')
	if horaPicoIni<HorarioApertura or horaPicoFin>HorarioCierre:
		return (False,'El horario pico debe estar dentro del horario de funcionamiento del estacionamiento')
	if Decimal(tarifa)>= Decimal(tarifaPico):
		return (False, 'La tarifa para el horario pico debe ser mayor que la tarifa para el horario valle')
	if horaPicoIni >= horaPicoFin:
		return (False, 'La hora de inicio de la hora pico debe ser menor que el fin de la hora pico')
	if horaPicoIni == HorarioApertura and horaPicoFin == HorarioCierre:
		return (False, 'Se debe garantizar la existencia de al menos un minuto de horario valle')
	return (True, '')

# Función que permite obtener el número de un recibo de pago determinado

def obtenerNumRecibo(estacionamiento):
    listaRecibo = ReciboPagoModel.objects.all()
    maxId = 0	
    for recibo in listaRecibo :
        if recibo.Reserva.Estacionamiento.id == estacionamiento.id :
            if maxId < recibo.numeroRecibo :
                maxId = recibo.numeroRecibo
    maxId= maxId+1
    return maxId		

# Función para verificar que la tarifa para el fin de semana existe, cuando el esquema tarifario es el
# Diferenciado por fin de semana

def validarFin(tarifa,tarifaFin):
	if tarifaFin is None:
		return (False,'La tarifa para el fin de semana es obligatoria')
	return (True,'')

def construirGrafico(tasasDia,estadistica,dia,tasasHora="",name=""):
    if tasasHora != "":
        aux = []
        for hora in range(len(tasasHora)):
            aux.append(float(tasasHora[hora]) + 0.5)
        ejeX = aux
        type = 25
        rangoIni = 0
        rangoFin = 24
        titulo = "Horas de reserva"
    else:
        titulo = "DÃ­aas de reserva"
        ejeX = tasasDia
        type = 15
        rangoIni = -0.5
        rangoFin = 7.5
    	
    data = Data([
        Bar(
            x = ejeX,
            y = estadistica,
        )
    ])


    layout = Layout(
        xaxis = XAxis(
            showline = True,
            rangemode = "nonnegative",
            title = titulo,
            nticks = type,
            range = [rangoIni,rangoFin],
            linewidth = 1,
            mirror = False,
            gridwidth = 1,
            zeroline = True,
            zerolinewidth = 0.1,
            gridcolor = "rgb(204, 204, 204)"
        ),
        yaxis = YAxis(
            type = "linear",
            range = [
            0,
            100
            ],
            autorange = False,
            showgrid = True,
            showline = True,
            rangemode = "nonnegative",
            title = "Porcentaje",
            linewidth = 1,
            mirror = False,
            gridwidth = 1,
            zeroline = True,
            zerolinewidth = 0.1,
            nticks = 20,
            dtick = 5,
            autotick = True,
            ticks = "inside",
            ticklen = 5,
            tickwidth = 1,
            gridcolor = "rgb(204, 204, 204)"
        ),
        height = 477,
        width = 811,
        autosize = True,
        showlegend = False,
        separators = ".,",
        margin = Margin(
            autoexpand = False
        ),
        plot_bgcolor = "rgb(255, 255, 255)",
        barmode = "stack",
        bargap = 0.1,
        bargroupgap = 0,
        paper_bgcolor = "rgb(255, 255, 255)",
    )

    fig = Figure(data=data,layout = layout)
    py.plot(fig, filename=name, auto_open=False) 
