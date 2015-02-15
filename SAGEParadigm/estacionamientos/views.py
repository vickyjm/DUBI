# -*- coding: utf-8 -*-

from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render

from django.utils import timezone

from estacionamientos.controller import *
from estacionamientos.forms import EstacionamientoExtendedForm
from estacionamientos.forms import EstacionamientoForm
from estacionamientos.forms import EstacionamientoReserva
from estacionamientos.forms import PagoReserva
from estacionamientos.models import Estacionamiento, ReservasModel
from time import strptime


listaReserva = []

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

def estacionamiento_detail(request, _id):
    _id = int(_id)
    # Verificamos que el objeto exista antes de continuar
    try:
        estacion = Estacionamiento.objects.get(id = _id)
    except ObjectDoesNotExist:
        return render(request, '404.html')

    global listaReserva
    listaReserva = []

    if request.method == 'POST':
            # Leemos el formulario
            form = EstacionamientoExtendedForm(request.POST)
            # Si el formulario
            if form.is_valid():
                hora_in = form.cleaned_data['horarioin']
                hora_out = form.cleaned_data['horarioout']
                reserva_in = form.cleaned_data['horario_reserin']
                reserva_out = form.cleaned_data['horario_reserout']

                m_validado = HorarioEstacionamiento(hora_in, hora_out, reserva_in, reserva_out)
                if not m_validado[0]:
                    return render(request, 'templateMensaje.html', {'color':'red', 'mensaje': m_validado[1]})

                estacion.Tarifa = form.cleaned_data['tarifa']
                estacion.Esquema = form.cleaned_data['esquema']
                estacion.Apertura = hora_in
                estacion.Cierre = hora_out
                estacion.Reservas_Inicio = reserva_in
                estacion.Reservas_Cierre = reserva_out
                estacion.NroPuesto = form.cleaned_data['puestos']

                estacion.save()
    else:
        form = EstacionamientoExtendedForm()

    return render(request, 'estacionamiento.html', {'form': form, 'estacionamiento': estacion})


def estacionamiento_reserva(request, _id):
    _id = int(_id)
    # Verificamos que el objeto exista antes de continuar
    try:
        estacion = Estacionamiento.objects.get(id = _id)
    except ObjectDoesNotExist:
        return render(request, '404.html')

    global listaReserva

    # Antes de entrar en la reserva, si la lista esta vacia, agregamos los
    # valores predefinidos
    if len(listaReserva) < 1:

        Puestos = ReservasModel.objects.filter(Estacionamiento = estacion).values_list('Puesto', 'InicioReserva', 'FinalReserva')
        elem1 = (datetime.datetime.min, datetime.datetime.min)
        elem2 = (datetime.datetime.max,datetime.datetime.max)
        listaReserva = [[elem1, elem2] for _ in range(estacion.NroPuesto)]
        
        for obj in Puestos:
            puesto = busquedaBin(obj[1], obj[2], listaReserva[obj[0]])
            listaReserva[obj[0]] = insertarReserva(obj[1], obj[2], puesto[0], listaReserva[obj[0]])


    # Si se hace un GET renderizamos los estacionamientos con su formulario
    if request.method == 'GET':
        form = EstacionamientoReserva()
        return render(request, 'estacionamientoReserva.html', {'form': form, 'estacionamiento': estacion})

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
                m_validado = validarHorarioReserva(inicio_reserva, final_reserva, estacion.Reservas_Inicio, estacion.Reservas_Cierre,datetime.datetime.now())

                # Si no es valido devolvemos el request
                if not m_validado[0]:
                    return render(request, 'templateMensaje.html', {'color':'red', 'mensaje': m_validado[1]})

                # Si esta en un rango valido, procedemos a buscar en la lista
                # el lugar a insertar
                x = buscar(inicio_reserva, final_reserva, listaReserva)
                if x[2] == True :
                    
                    request.session['puesto'] = x[0]
                    request.session['inicioR'] = inicio_reserva.strftime('%Y-%m-%d %H:%M:%S')
                    request.session['finalR'] = final_reserva.strftime('%Y-%m-%d %H:%M:%S')
                    
#                     reservar(inicio_reserva, final_reserva, listaReserva)
#                     reservaFinal = ReservasModel(
#                                         Estacionamiento = estacion,
#                                         Puesto = x[0],
#                                         InicioReserva = inicio_reserva,
#                                         FinalReserva = final_reserva
#                                     )
#                     reservaFinal.save()
                    tarifaCosto=int(estacion.Tarifa)
                    tarifaFinal=0
                    if estacion.Esquema == 'Hora' or estacion.Esquema=='hora':
                        tarifaFinal=calculoTarifaHora(inicio_reserva,final_reserva,tarifaCosto)
                    elif estacion.Esquema == 'Minuto' or estacion.Esquema == 'minuto':
                        tarifaFinal = calculoTarifaMinuto(inicio_reserva, final_reserva, tarifaCosto)
                        
                    request.session['monto'] = tarifaFinal
                    mensajeTarifa='La solicitud es factible. El costo es de ' + str(tarifaFinal)+" BsF"
                    return render(request, 'reservaFactible.html', {'color':'green', 'mensaje': mensajeTarifa})
                else:
                    return render(request, 'templateMensaje.html', {'color':'red', 'mensaje':'No hay un puesto disponible para ese horario'})
    else:
        form = EstacionamientoReserva()

    return render(request, 'estacionamientoReserva.html', {'form': form, 'estacionamiento': estacion})

def estacionamiento_pagar_reserva(request, _id):
    _id = int(_id)
    # Verificamos que el objeto exista antes de continuar
    try:
        estacion = Estacionamiento.objects.get(id = _id)
    except ObjectDoesNotExist:
        return render(request, '404.html')
    
    puesto = request.session.get('puesto')
    inicio_reserva = request.session.get('inicioR')
    final_reserva = request.session.get('finalR')
    monto = request.session.get('monto')
    datetime.datetime.strptime(inicio_reserva,'%Y-%m-%d %H:%M:%S')
    datetime.datetime.strptime(final_reserva,'%Y-%m-%d %H:%M:%S')
    request.session.flush()
    
    if request.method == 'GET':
        form = PagoReserva()
        return render(request, 'pagoReserva.html', {'form': form, 'estacionamiento': estacion,'inicio': inicio_reserva,'final': final_reserva,'monto': monto})
    elif request.method == 'POST':
        form = PagoReserva(request.POST)
        
        # Verificamos si es valido con los validadores del formulario
        if form.is_valid():
            tipoTarjeta = form.cleaned_data['tipoTarjeta']
            numTarjeta = form.cleaned_data['numTarjeta']
            
            reservar(inicio_reserva, final_reserva, listaReserva)
            reservaFinal = ReservasModel(
                                Estacionamiento = estacion,
                                Puesto = puesto,
                                InicioReserva = inicio_reserva,
                                FinalReserva = final_reserva
                            )
            reservaFinal.save()
            
            mensajeExito = 'La reserva fue realizada con exito'
            return render(request, 'templateMensaje.html', {'color':'green', 'mensaje': mensajeExito})
    else : 
        form = PagoReserva()
    return render(request, 'pagoReserva.html', {'form': form, 'estacionamiento': estacion,'inicio': inicio_reserva,'final': final_reserva,'monto': monto})
    