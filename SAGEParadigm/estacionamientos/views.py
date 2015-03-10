# -*- coding: utf-8 -*-

from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render

from django.utils import timezone
from operator import attrgetter
from estacionamientos.controller import *
from estacionamientos.forms import EstacionamientoExtendedForm
from estacionamientos.forms import EstacionamientoForm
from estacionamientos.forms import EstacionamientoReserva
from estacionamientos.forms import ConsultarIngresoForm
from estacionamientos.forms import ConsultarReservasForm
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
    if (estacion.Apertura != None):
        hApertura = str(estacion.Apertura.hour) + ':' + str(estacion.Apertura.minute)
        hCierre = str(estacion.Cierre.hour) + ':' + str(estacion.Cierre.minute)
        if (estacion.Esquema == 'DifHora'):
            pIni = str(esq.PicoIni.hour) + ':' + str(esq.PicoIni.minute)
            pFin = str(esq.PicoFin.hour) + ':' + str(esq.PicoFin.minute)
            return render(request, 'estacionamiento.html', {'form': form, 'esquemaform': esquemaform, 'estacionamiento': estacion, 'esquema': esq,'hApertura':hApertura,'hCierre':hCierre,"pIni":pIni,"pFin":pFin})
        return render(request, 'estacionamiento.html', {'form': form, 'esquemaform': esquemaform, 'estacionamiento': estacion, 'esquema': esq,'hApertura':hApertura,'hCierre':hCierre})    
    return render(request, 'estacionamiento.html', {'form': form, 'esquemaform': esquemaform, 'estacionamiento': estacion, 'esquema': esq})

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
    tasasDia = []
    horasApertura = []    
    if estacion.Cierre.hour == 23 and estacion.Cierre.minute > 0:
        longFin = 24
    else:
        longFin = estacion.Cierre.hour
    for i in range(estacion.Apertura.hour,longFin):
        horasApertura.append(i)
    
    diasSemana = {0:'Lunes',1:'Martes',2:'Miércoles',3:'Jueves',4:'Viernes',5:'Sábado',6:'Domingo'}
    weekDay = datetime.datetime.now().weekday()

    estadistica = calcularTasaReservaHoras(listaReserva, estacion.Apertura, estacion.Cierre,estacion.NroPuesto,datetime.datetime.now())
    porcentaje = 0
    diasReserva = []
    for dia in range(0,8):
        for i in range(len(estadistica[dia])):
            estadistica[dia][i] = float(estadistica[dia][i])
            porcentaje += estadistica[dia][i]
        temp=(datetime.datetime.now()+datetime.timedelta(days=dia)).date()
        tasasDia.append(str(temp.day)+"-"+str(temp.month)+"-"+str(temp.year))
        if weekDay == 6: weekDay = -1
        weekDay += 1
        diasReserva.append(porcentaje/len(horasApertura)) 
        porcentaje = 0
            
    now = datetime.datetime.now()
    fechaActual = str(now.day)+"-"+str(now.month)+"-"+str(now.year)
    construirGrafico(tasasDia, diasReserva,fechaActual)
    return render(request, 'tasaOcupacion.html', \
                  {'estacionamiento': estacion, 'horas': horasApertura, 'dias': \
                   tasasDia, 'estadisticas': estadistica, 'fechaActual': fechaActual})
    
def estacionamiento_ingreso(request):
    if request.method == 'GET':
        form = ConsultarIngresoForm()
        return render(request,'consultarIngresos.html', {'form': form})
    elif request.method == 'POST':
        form = ConsultarIngresoForm(request.POST)
        if form.is_valid():
            Rif = form.cleaned_data['rif']
            listEst = []
            listEst = obtenerIngresos(Rif)
            total = 0
            for obj in listEst :
                total = total+obj[1]
                obj[1] = '{0:,}'.format(obj[1])
            total = '{0:,}'.format(total)
            return render(request, 'mostrarIngresos.html', {'form': form,'ingresos': listEst,'total': total})
    else:
            form = ConsultarIngresoForm()
    return render(request,'consultarIngresos.html', {'form': form})

def consultar_reservas(request):
    
    if request.method == 'GET':
        form = ConsultarReservasForm()
        return render(request, 'consultarReservas.html', {'form': form})
    elif request.method == 'POST':
        form = ConsultarReservasForm(request.POST)
        if form.is_valid():
            nac = form.cleaned_data['nacionalidad']
            ci = form.cleaned_data['cedula']
            cedulaCompleta = nac + ci
            recibos = sorted(ReciboPagoModel.objects.filter(cedula = cedulaCompleta),key=attrgetter('Reserva.InicioReserva'))
            return render(request,'mostrarReservas.html',{'recibos': recibos})
    else : 
            form = ConsultarReservasForm()
    
    return render(request, 'consultarReservas.html', {'form': form})
