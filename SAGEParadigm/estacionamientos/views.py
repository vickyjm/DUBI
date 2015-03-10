# -*- coding: utf-8 -*-

from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render

from django.utils import timezone

from estacionamientos.controller import *
from estacionamientos.forms import EstacionamientoExtendedForm
from estacionamientos.forms import EstacionamientoForm
from estacionamientos.forms import EstacionamientoReserva

from estacionamientos.forms import PagoReserva
from estacionamientos.forms import EsquemaForm
from time import strptime
from estacionamientos.models import *
from django.db.models.lookups import Day
from _datetime import date

listaReserva = [] # Cada reserva está representada por un par de listas de la forma [inicio,-1],[fin,1]

# Usamos esta vista para procesar todos los estacionamientos
def estacionamientos_all(request):
    global listaReserva
    listaReserva = []
    # Si se hace un POST a esta vista implica que se quiere agregar un nuevo
    # estacionamiento
    estacionamientos = Estacionamiento.objects.all()
    if request.method == 'POST':
            # Creamos un formulario con los datos que recibimos
            form = EstacionamientoForm(request.POST)

            # Parte de la entrega era limitar la cantidad maxima de
            # estacionamientos a 5
            if len(estacionamientos) >= 5:
                    return render(request, 'templateMensaje.html',
                                  {'color':'red', 'mensaje':'No se pueden agregar más estacionamientos'})

            # Si el formulario es valido, entonces creamos un objeto con
            # el constructor del modelo
            if form.is_valid():
                obj = Estacionamiento(
                        Propietario = form.cleaned_data['propietario'],
                        Nombre = form.cleaned_data['nombre'],
                        Direccion = form.cleaned_data['direccion'],
                        Rif = form.cleaned_data['rif'],
                        Telefono_1 = form.cleaned_data['telefono_1'],
                        Telefono_2 = form.cleaned_data['telefono_2'],
                        Telefono_3 = form.cleaned_data['telefono_3'],
                        Email_1 = form.cleaned_data['email_1'],
                        Email_2 = form.cleaned_data['email_2']
                )
                obj.save()
                # Recargamos los estacionamientos ya que acabamos de agregar
                estacionamientos = Estacionamiento.objects.all()
    # Si no es un POST es un GET, y mandamos un formulario vacio
    else:
        form = EstacionamientoForm()

    return render(request, 'base.html',{'form': form, 'estacionamientos': estacionamientos})

# Vista para realizar la parametrización de un estacionamiento
def estacionamiento_detail(request, _id):
    _id = int(_id)
    # Verificamos que el objeto exista antes de continuar
    try:
        estacion = Estacionamiento.objects.get(id = _id)
        esq = Esquema(Estacionamiento = estacion, Tarifa = Decimal(0))
        if estacion.Esquema: # Si el estacionamiento ya tiene un esquema, se usa 
            esq=eval(estacion.Esquema+".objects.get(Estacionamiento=estacion)")            
    except ObjectDoesNotExist:
        return render(request, '404.html')

    global listaReserva
    listaReserva = []
    
    if request.method == 'POST':
            # Leemos el formulario
            form = EstacionamientoExtendedForm(request.POST)
            esquemaform = EsquemaForm(request.POST)
            # Si el formulario es valido
            if form.is_valid():
                hora_in = form.cleaned_data['horarioin']
                hora_out = form.cleaned_data['horarioout']

                m_validado = HorarioEstacionamiento(hora_in, hora_out)
                if not m_validado[0]:
                    return render(request, 'templateMensaje.html', \
                                  {'color':'red', 'mensaje': m_validado[1], 'estacionamiento':estacion})                
                if esquemaform.is_valid():    
                    tipoEsquema=esquemaform.cleaned_data['esquema']
                    tarifa = esquemaform.cleaned_data['tarifa']
                    if estacion.Esquema:
                        eval(tipoEsquema+".objects.filter(Estacionamiento=estacion).delete()")
                    if tipoEsquema=="DifHora":
                        picoIni = esquemaform.cleaned_data['hora_picoini']
                        picoFin = esquemaform.cleaned_data['hora_picofin']
                        tarifaPico = esquemaform.cleaned_data['tarifa_pico']
                        m_validado=validarPicos(hora_in,hora_out,picoIni,picoFin,tarifa,tarifaPico)
                        if not m_validado[0]:
                            return render(request, 'templateMensaje.html', \
                                    {'color':'red', 'mensaje': m_validado[1], 'estacionamiento':estacion})
                        esq = eval(tipoEsquema+"(Estacionamiento=estacion,Tarifa=tarifa,\
                                                PicoIni=picoIni,PicoFin=picoFin,TarifaPico=tarifaPico)")
                    elif tipoEsquema=="DifFin":
                        tarifaFin = esquemaform.cleaned_data['tarifa_fin']
                        m_validado=validarFin(tarifa,tarifaFin)
                        if not m_validado[0]:
                            return render(request, 'templateMensaje.html', \
                                          {'color':'red', 'mensaje': m_validado[1]})
                        esq = eval(tipoEsquema+"(Estacionamiento = estacion, Tarifa = tarifa, \
                                                                        TarifaFin = tarifaFin)")
                    else:
                        esq=eval(tipoEsquema+"(Estacionamiento = estacion, Tarifa = tarifa)")
                    esq.save()
                    estacion.Esquema = esquemaform.cleaned_data['esquema']
                    estacion.Apertura = hora_in
                    estacion.Cierre = hora_out
                    estacion.NroPuesto = form.cleaned_data['puestos']
                    estacion.save()
    else:
        form = EstacionamientoExtendedForm()
        esquemaform = EsquemaForm()
    return render(request, 'estacionamiento.html', \
                  {'form': form, 'esquemaform': esquemaform, 'estacionamiento': estacion, 'esquema': esq})

# Vista para procesar una reserva en un estacionamiento
def estacionamiento_reserva(request, _id):
    _id = int(_id)
    # Verificamos que el objeto exista antes de continuar
    try:
        estacion = Estacionamiento.objects.get(id = _id)
        esq=eval(estacion.Esquema+".objects.get(Estacionamiento = estacion)")
    except ObjectDoesNotExist:
        return render(request, '404.html')

    global listaReserva

    # Si se hace un GET renderizamos los estacionamientos con su formulario
    if request.method == 'GET':
        form = EstacionamientoReserva()
        return render(request, 'estacionamientoReserva.html', \
                      {'form': form, 'estacionamiento': estacion, 'esquema': esq})

    # Si es un POST estan mandando un request
    elif request.method == 'POST':
            form = EstacionamientoReserva(request.POST)
            # Verificamos si es valido con los validadores del formulario
            if form.is_valid():
                fechaIni = form.cleaned_data['fechaInicio']
                horaIni = form.cleaned_data['horaInicio']
                fechaFin = form.cleaned_data['fechaFinal']
                horaFin = form.cleaned_data['horaFinal']
                
                inicio_reserva = datetime.datetime.combine(fechaIni,horaIni)
                final_reserva = datetime.datetime.combine(fechaFin,horaFin)

                # Validamos los horarios con los horario de salida y entrada
                m_validado = validarHorarioReserva(inicio_reserva, final_reserva, \
                                            estacion.Apertura, estacion.Cierre,datetime.datetime.now())

                # Si no es valido devolvemos el request
                if not m_validado[0]:
                    return render(request, 'templateMensaje.html', \
                                {'color':'red', 'mensaje': m_validado[1], 'estacionamiento':estacion})
                # Antes de entrar en la reserva, si la lista esta vacia, agregamos los valores predefinidos
                if len(listaReserva) < 1:          
                    puestos = ReservasModel.objects.filter(Estacionamiento = estacion).values_list('InicioReserva', 'FinalReserva')
                    for obj in puestos:
                        listaReserva.append([obj[0],-1])
                        listaReserva.append([obj[1],1])                        
                # Si esta en un rango valido, procedemos a buscar en la lista el lugar a insertar
                exito = reservar(inicio_reserva, final_reserva, listaReserva, estacion.NroPuesto)
                
                if exito == True :
                    
                    # Creamos una sesion para pasar informacion a la siguiente view
                    request.session['inicioR'] = inicio_reserva.strftime('%Y-%m-%d %H:%M:%S')
                    request.session['finalR'] = final_reserva.strftime('%Y-%m-%d %H:%M:%S')
                    
                    tarifaFinal=esq.calcularMonto(inicio_reserva,final_reserva)
                    tarifaFinal=float(tarifaFinal)
                    request.session['monto'] = tarifaFinal
                    mensajeTarifa='La solicitud es factible. El costo es de ' + str(tarifaFinal)+" BsF"
                
                    return render(request, 'reservaFactible.html', \
                                  {'color':'green', 'mensaje': mensajeTarifa, 'estacionamiento':estacion})                
                else:
                    return render(request, 'templateMensaje.html', \
                        {'color':'red', 'mensaje':'No hay un puesto disponible para ese horario', \
                            'estacionamiento':estacion})
                
    else:
        form = EstacionamientoReserva()

    return render(request, 'estacionamientoReserva.html', \
                  {'form': form, 'estacionamiento': estacion, 'esquema': esq})

# Vista para realizar el pago de una reserva y generar el recibo asociado
def estacionamiento_pagar_reserva(request, _id):
    _id = int(_id)
    
    # Verificamos que el objeto exista antes de continuar
    try:
        estacion = Estacionamiento.objects.get(id = _id)
    except ObjectDoesNotExist:
        return render(request, '404.html')
    
    global listaReserva
    
    # Pedimos los datos de la sesion creada por la view anterior
    inicio_reserva = request.session.get('inicioR')
    final_reserva = request.session.get('finalR')
    monto = request.session.get('monto')
    
    inicio_reserva=datetime.datetime.strptime(inicio_reserva,'%Y-%m-%d %H:%M:%S')
    final_reserva=datetime.datetime.strptime(final_reserva,'%Y-%m-%d %H:%M:%S')
    
    if request.method == 'GET':
        form = PagoReserva()
        return render(request, 'pagoReserva.html', \
                        {'form': form, 'estacionamiento': estacion,\
                         'inicio': inicio_reserva,'final': final_reserva,'monto': monto})
    elif request.method == 'POST':
        form = PagoReserva(request.POST)
        
        # Verificamos si es valido con los validadores del formulario
        if form.is_valid():
            nombreCliente = form.cleaned_data['nombre']
            apellidoCliente = form.cleaned_data['apellidos']
            nacionalidadCliente = form.cleaned_data['nacionalidad']
            cedulaCliente = form.cleaned_data['cedula']
            tipoTarjeta = form.cleaned_data['tipoTarjeta']
            numTarjeta = form.cleaned_data['numTarjeta']
            
            listaReserva.append([inicio_reserva,-1])    # Se agregan las horas aceptadas a la lista 
                                                        # de las reservas
            listaReserva.append([final_reserva,1])
            
            # Creamos los objetos de reserva y pago y los guardamos en la base de datos.
            reservaFinal = ReservasModel(
                                Estacionamiento = estacion,
                                InicioReserva = inicio_reserva,
                                FinalReserva = final_reserva
                            )
            reservaFinal.save()
            
            numRecibo = obtenerNumRecibo(estacion)
            
            pago = ReciboPagoModel(
                               numeroRecibo = numRecibo,
                               Reserva = reservaFinal,
                               cedula = nacionalidadCliente + cedulaCliente,
                               fechaTransaccion = datetime.datetime.now(),
                               TipoTarjeta = tipoTarjeta,
                               MontoPago = Decimal(monto).quantize(Decimal(10)**-2)
                            )
            pago.save()
            
            mensajeExito = 'Su reserva ha sido exitosa. Este es su recibo de pago :'
            return render(request, 'mostrarRecibo.html', \
                    {'recibo': pago,'color': 'green','mensaje' : mensajeExito, \
                                                    'estacionamiento':estacion})
    else : 
        form = PagoReserva()
    return render(request, 'pagoReserva.html', \
                {'form': form, 'estacionamiento': estacion,'inicio': \
                    inicio_reserva,'final': final_reserva,'monto': monto})
    
# Vista para mostrar la tasa de ocupación de un estacionamiento según cierta granularidad
def estacionamiento_tasa_ocupacion(request, _id):
    _id = int(_id)
    # Verificamos que el objeto exista antes de continuar
    estacionamientos = Estacionamiento.objects.all()
    try:
        estacion = Estacionamiento.objects.get(id = _id)
    except ObjectDoesNotExist:
        return render(request, '404.html')
 
    global listaReserva
    
    # Se llena la lista de reservas
    if len(listaReserva) < 1:          
        puestos = ReservasModel.objects.filter(Estacionamiento = estacion).values_list('InicioReserva', 'FinalReserva')
        for obj in puestos:
            listaReserva.append([obj[0],-1])
            listaReserva.append([obj[1],1]) 
    now = datetime.datetime.now()             
    tasasDia = []
    horasApertura = []    
    if estacion.Cierre.hour == 23 and estacion.Cierre.minute > 0:
        longFin = 24
    else:
        longFin = estacion.Cierre.hour
    for i in range(estacion.Apertura.hour,longFin):
        horasApertura.append(i)
    
    weekDay = now.weekday()

    estadistica = calcularTasaReservaHoras(listaReserva, estacion.Apertura, estacion.Cierre,estacion.NroPuesto,now)
    porcentaje = 0
    diasReserva = []
    for dia in range(0,8):
        for i in range(len(estadistica[dia])):
            estadistica[dia][i] = float(estadistica[dia][i])
            porcentaje += estadistica[dia][i]
        temp=(now+datetime.timedelta(days=dia)).date()
        tasasDia.append(str(temp.day)+"-"+str(temp.month)+"-"+str(temp.year))
        if weekDay == 6: weekDay = -1
        weekDay += 1
        conversion = float(Decimal('%.1f' % (porcentaje/len(horasApertura))))
        diasReserva.append(conversion)  
        porcentaje = 0
            

    fechaActual = str(now.day)+"-"+str(now.month)+"-"+str(now.year)
    return render(request, 'tasaOcupacion.html', \
                  {'estacionamiento': estacion, 'horas': horasApertura, 'dias': \
                   tasasDia, 'estadisticas': estadistica, 'fechaActual': fechaActual})



# Vista para mostrar la grafica de la tasa de ocupación de un estacionamiento según granularidad dia
def estacionamiento_tasa_ocupacion_dia(request, _id):
    _id = int(_id)
    # Verificamos que el objeto exista antes de continuar
    estacionamientos = Estacionamiento.objects.all()
    try:
        estacion = Estacionamiento.objects.get(id = _id)
    except ObjectDoesNotExist:
        return render(request, '404.html')
 
    global listaReserva
    
    # Se llena la lista de reservas
    if len(listaReserva) < 1:          
        puestos = ReservasModel.objects.filter(Estacionamiento = estacion).values_list('InicioReserva', 'FinalReserva')
        for obj in puestos:
            listaReserva.append([obj[0],-1])
            listaReserva.append([obj[1],1]) 
         
    now = datetime.datetime.now()  
    tasasDia = []
    horasApertura = []    
    if estacion.Cierre.hour == 23 and estacion.Cierre.minute > 0:
        longFin = 24
    else:
        longFin = estacion.Cierre.hour
    for i in range(estacion.Apertura.hour,longFin):
        horasApertura.append(i)
    
    weekDay = now.weekday()

    estadistica = calcularTasaReservaHoras(listaReserva, estacion.Apertura, estacion.Cierre,estacion.NroPuesto,now)
    porcentaje = 0
    diasReserva = []
    for dia in range(0,8):
        for i in range(len(estadistica[dia])):
            estadistica[dia][i] = float(estadistica[dia][i])
            porcentaje += estadistica[dia][i]
        temp=(now+datetime.timedelta(days=dia)).date()
        tasasDia.append(str(temp.day)+"-"+str(temp.month)+"-"+str(temp.year))
        if weekDay == 6: weekDay = -1
        weekDay += 1
        conversion = float(Decimal('%.1f' % (porcentaje/len(horasApertura))))
        diasReserva.append(conversion) 
        porcentaje = 0
            
    fechaActual = str(now.day)+"-"+str(now.month)+"-"+str(now.year)

    # por grano dias
    construirGrafico(tasasDia, diasReserva,fechaActual,"","1")
      
    return render(request, 'tasaOcupacionDia.html', \
                  {'estacionamiento': estacion, 'horas': horasApertura, 'dias': \
                   tasasDia, 'estadisticas': estadistica, 'fechaActual': fechaActual})



# Vista para mostrar las graficas de la tasa de ocupación de un estacionamiento según granularidad horas
def estacionamiento_tasa_ocupacion_hora(request, _id):
    _id = int(_id)
    # Verificamos que el objeto exista antes de continuar
    estacionamientos = Estacionamiento.objects.all()
    try:
        estacion = Estacionamiento.objects.get(id = _id)
    except ObjectDoesNotExist:
        return render(request, '404.html')
 
    global listaReserva
    
    # Se llena la lista de reservas
    if len(listaReserva) < 1:          
        puestos = ReservasModel.objects.filter(Estacionamiento = estacion).values_list('InicioReserva', 'FinalReserva')
        for obj in puestos:
            listaReserva.append([obj[0],-1])
            listaReserva.append([obj[1],1]) 
    now = datetime.datetime.now()             
    tasasDia = []
    horasApertura = []    
    if estacion.Cierre.hour == 23 and estacion.Cierre.minute > 0:
        longFin = 24
    else:
        longFin = estacion.Cierre.hour
    for i in range(estacion.Apertura.hour,longFin):
        horasApertura.append(i)
    
    weekDay = now.weekday()

    estadistica = calcularTasaReservaHoras(listaReserva, estacion.Apertura, estacion.Cierre,estacion.NroPuesto,now)
    porcentaje = 0
    diasReserva = []
    for dia in range(0,8):
        for i in range(len(estadistica[dia])):
            estadistica[dia][i] = float(estadistica[dia][i])
            porcentaje += estadistica[dia][i]
        temp=(now+datetime.timedelta(days=dia)).date()
        tasasDia.append(str(temp.day)+"-"+str(temp.month)+"-"+str(temp.year))
        if weekDay == 6: weekDay = -1
        weekDay += 1
        conversion = float(Decimal('%.1f' % (porcentaje/len(horasApertura))))
        diasReserva.append(conversion)  
        porcentaje = 0

    fechaActual = str(now.day)+"-"+str(now.month)+"-"+str(now.year)

    # por grano horas
    construirGrafico("",estadistica[0],fechaActual,horasApertura,"2")
    construirGrafico("",estadistica[1],fechaActual,horasApertura,"3")
    construirGrafico("",estadistica[2],fechaActual,horasApertura,"4")
    construirGrafico("",estadistica[3],fechaActual,horasApertura,"5")
    construirGrafico("",estadistica[4],fechaActual,horasApertura,"6")
    construirGrafico("",estadistica[5],fechaActual,horasApertura,"7")
    construirGrafico("",estadistica[6],fechaActual,horasApertura,"8")
    construirGrafico("",estadistica[7],fechaActual,horasApertura,"9")        
    return render(request, 'tasaOcupacionHora.html', \
                  {'estacionamiento': estacion, 'horas': horasApertura, 'dias': \
                   tasasDia, 'estadisticas': estadistica, 'fechaActual': fechaActual})