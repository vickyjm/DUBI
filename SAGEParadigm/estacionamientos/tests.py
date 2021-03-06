# -*- coding: utf-8 -*-

import datetime
from django.test import Client
from django.test import TestCase
import unittest

from estacionamientos.controller import *
from estacionamientos.forms import *
from estacionamientos.forms import *
from estacionamientos.models import *
import django
django.setup()

###################################################################
#                    ESTACIONAMIENTO VISTA DISPONIBLE
###################################################################
class SimpleTest(unittest.TestCase):
	# normal
	def setUp(self):
		self.client = Client()

	# normal
	def test_primera(self):
		response = self.client.get('/estacionamientos/')
		self.assertEqual(response.status_code, 200)



###################################################################
#                    Pruebas para EstacionamientoForm
###################################################################

class EstacionamientoFormTestCase(TestCase):

	# malicia
	def test_CamposVacios(self):
		form_data = {}
		form = EstacionamientoForm(data = form_data)
		self.assertEqual(form.is_valid(), False)

	# caso borde
	def test_SoloUnCampoNecesario(self):
		form_data = {
			'propietario': 'Pedro'
		}
		form = EstacionamientoForm(data = form_data)
		self.assertEqual(form.is_valid(), False)

	# caso borde
	def test_DosCamposNecesarios(self):
		form_data = {
			'propietario': 'Pedro',
			'nombre': 'Orinoco'
		}
		form = EstacionamientoForm(data = form_data)
		self.assertEqual(form.is_valid(), False)

	# caso borde
	def test_TresCamposNecesarios(self):
		form_data = {
			'propietario': 'Pedro',
			'nombre': 'Orinoco',
			'direccion': 'Caracas'
		}
		form = EstacionamientoForm(data = form_data)
		self.assertEqual(form.is_valid(), False)

	# caso borde
	def test_TodosLosCamposNecesarios(self):
		form_data = {
			'propietario': 'Pedro',
			'nombre': 'Orinoco',
			'direccion': 'Caracas',
			'rif': 'V-12345678-9'
		}
		form = EstacionamientoForm(data = form_data)
		self.assertEqual(form.is_valid(), True)

	# malicia
	def test_PropietarioInvalidoDigitos(self):
		form_data = {
			'propietario': 'Pedro132',
			'nombre': 'Orinoco',
			'direccion': 'Caracas',
			'rif': 'V123456789'
		}
		form = EstacionamientoForm(data = form_data)
		self.assertEqual(form.is_valid(), False)

	# malicia
	def test_PropietarioInvalidoSimbolos(self):
		form_data = {
			'propietario': 'Pedro!',
			'nombre': 'Orinoco',
			'direccion': 'Caracas',
			'rif': 'V123456789'
		}
		form = EstacionamientoForm(data = form_data)
		self.assertEqual(form.is_valid(), False)

	# caso borde
	def test_RifTamanoInvalido(self):
		form_data = {
			'propietario': 'Pedro132',
			'nombre': 'Orinoco',
			'direccion': 'Caracas',
			'rif': 'V1234567'
		}
		form = EstacionamientoForm(data = form_data)
		self.assertEqual(form.is_valid(), False)

	# malicia
	def test_RifFormatoInvalido(self):
		form_data = {
			'propietario': 'Pedro132',
			'nombre': 'Orinoco',
			'direccion': 'Caracas',
			'rif': 'Kaa123456789'
		}
		form = EstacionamientoForm(data = form_data)
		self.assertEqual(form.is_valid(), False)

	# malicia
	def test_AgregarTelfs(self):
		form_data = {
			'propietario': 'Pedro',
			'nombre': 'Orinoco',
			'direccion': 'Caracas',
			'rif': 'V-12345678-9',
			'telefono_1': '0212-9322878',
			'telefono_2': '0414-9322878',
			'telefono_3': '0412-9322878'
		}
		form = EstacionamientoForm(data = form_data)
		self.assertEqual(form.is_valid(), True)

	# malicia
	def test_FormatoInvalidoTelf(self):
		form_data = {
			'propietario': 'Pedro',
			'nombre': 'Orinoco',
			'direccion': 'Caracas',
			'rif': 'V123456789',
			'telefono_1': '02119322878'
		}
		form = EstacionamientoForm(data = form_data)
		self.assertEqual(form.is_valid(), False)

	# caso borde
	def test_TamanoInvalidoTelf(self):
		form_data = {
			'propietario': 'Pedro',
			'nombre': 'Orinoco',
			'direccion': 'Caracas',
			'rif': 'V123456789',
			'telefono_1': '0219322878'
		}
		form = EstacionamientoForm(data = form_data)
		self.assertEqual(form.is_valid(), False)

	# malicia
	def test_AgregarCorreos(self):
		form_data = {
			'propietario': 'Pedro',
			'nombre': 'Orinoco',
			'direccion': 'Caracas',
			'rif': 'V-12345678-9',
			'telefono_1': '0212-9322878',
			'telefono_2': '0414-9322878',
			'telefono_3': '0412-9322878',
			'email_1': 'adminsitrador@admin.com',
			'email_2': 'usua_rio@users.com'
		}
		form = EstacionamientoForm(data = form_data)
		self.assertEqual(form.is_valid(), True)

	# malicia
	def test_CorreoInvalido(self):
		form_data = {
			'propietario': 'Pedro',
			'nombre': 'Orinoco',
			'direccion': 'Caracas',
			'rif': 'V123456789',
			'telefono_1': '02129322878',
			'telefono_2': '04149322878',
			'telefono_3': '04129322878',
			'email_1': 'adminsitrador@a@dmin.com'
		}
		form = EstacionamientoForm(data = form_data)
		self.assertEqual(form.is_valid(), False)

###################################################################
#                 Pruebas para Estacionamiento_ExtendedForm
###################################################################

class EstacionamientoExtendedFormTestCase(TestCase):
	
	# malicia
	def test_EstacionamientoExtendedForm_UnCampo(self):
		form_data = { 'puestos': 2}
		form = EstacionamientoExtendedForm(data = form_data)
		self.assertEqual(form.is_valid(), False)

	# malicia
	def test_EstacionamientoExtendedForm_DosCampos(self):
		form_data = { 'puestos': 2,
								'horarioin': datetime.time(6, 0)}
		form = EstacionamientoExtendedForm(data = form_data)
		self.assertEqual(form.is_valid(), False)

	# malicia
	def test_EstacionamientoExtendedForm_TodosCamposBien(self):
		form_data = { 'puestos': 2,
								'horarioin': datetime.time(6, 0),
								'horarioout': datetime.time(19, 0)}
		form = EstacionamientoExtendedForm(data = form_data)
		self.assertEqual(form.is_valid(), True)

	# caso borde
	def test_EstacionamientoExtendedForm_Puestos0(self):
		form_data = { 'puestos': 0,
								'horarioin': datetime.time(6, 0),
								'horarioout': datetime.time(19, 0),}
		form = EstacionamientoExtendedForm(data = form_data)
		self.assertEqual(form.is_valid(), True)

	# caso borde
	def test_EstacionamientoExtendedForm_HoraInicioIgualHoraCierre(self):
		form_data = { 'puestos': 2,
								'horarioin': datetime.time(6, 0),
								'horarioout': datetime.time(6, 0)}
		form = EstacionamientoExtendedForm(data = form_data)
		self.assertEqual(form.is_valid(), True)

	# malicia
	def test_EstacionamientoExtendedForm_StringEnPuesto(self):
		form_data = { 'puestos': 'hola',
								'horarioin': datetime.time(6, 0),
								'horarioout': datetime.time(19, 0)}
		form = EstacionamientoExtendedForm(data = form_data)
		self.assertEqual(form.is_valid(), False)

	# malicia
	def test_EstacionamientoExtendedForm_StringHoraInicio(self):
		form_data = { 'puestos': 2,
								'horarioin': 'holaa',
								'horarioout': datetime.time(19, 0)}
		form = EstacionamientoExtendedForm(data = form_data)
		self.assertEqual(form.is_valid(), False)

	# malicia
	def test_EstacionamientoExtendedForm_NumeroNegativoHoraInicio(self):
		form_data = { 'puestos': 2,
								'horarioin':-1,
								'horarioout': datetime.time(19, 0)}
		form = EstacionamientoExtendedForm(data = form_data)
		self.assertEqual(form.is_valid(), False)


	# malicia
	def test_EstacionamientoExtendedForm_NoneEnHorarioCierre(self):
		form_data = { 'puestos': 2,
								'horarioin': 'holaa',
								'horarioout': None}
		form = EstacionamientoExtendedForm(data = form_data)
		self.assertEqual(form.is_valid(), False)

	# malicia
	def test_EstacionamientoExtendedForm_listaEnHoraApertura(self):

		form_data = { 'puestos': 2,
								'horarioin': [datetime.time(6, 0)],
								'horarioout': datetime.time(19, 0)}
		form = EstacionamientoExtendedForm(data = form_data)
		self.assertEqual(form.is_valid(), False)

######################################################################
# Pruebas para el controlador de EstacionamientoExtendedForm
#####################################################################

class EstacionamientoExtendedFormControllerTestCase(TestCase):
	
	# normal
	def test_HorariosValidos(self):
		HoraInicio = datetime.time(hour = 12, minute = 0, second = 0)
		HoraFin = datetime.time(hour = 18, minute = 0, second = 0)
		x = HorarioEstacionamiento(HoraInicio, HoraFin)
		self.assertEqual(x, (True, ''))

	# malicia
	def test_HorariosInvalido_HoraCierre_Menor_HoraApertura(self):
		HoraInicio = datetime.time(hour = 12, minute = 0, second = 0)
		HoraFin = datetime.time(hour = 11, minute = 0, second = 0)
		x = HorarioEstacionamiento(HoraInicio, HoraFin)
		self.assertEqual(x, (False, 'El horario de apertura debe ser menor al horario de cierre'))

	# caso borde
	def test_HorariosInvalido_HoraCierre_Igual_HoraApertura(self):
		HoraInicio = datetime.time(hour = 12, minute = 0, second = 0)
		HoraFin = datetime.time(hour = 12, minute = 0, second = 0)
		x = HorarioEstacionamiento(HoraInicio, HoraFin)
		self.assertEqual(x, (False, 'El horario de apertura debe ser menor al horario de cierre'))

	# caso borde
	def test_Limite_HorarioValido_Apertura_Cierre(self):
		HoraInicio = datetime.time(hour = 12, minute = 0, second = 0)
		HoraFin = datetime.time(hour = 12, minute = 0, second = 1)
		x = HorarioEstacionamiento(HoraInicio, HoraFin)
		self.assertEqual(x, (True, ''))

	# caso borde
	def test_Limite_Superior_HorarioValido_Apertura_Cierre(self):
		HoraInicio = datetime.time(hour = 0, minute = 0, second = 0)
		HoraFin = datetime.time(hour = 23, minute = 59, second = 59)
		x = HorarioEstacionamiento(HoraInicio, HoraFin)
		self.assertEqual(x, (True, ''))

###################################################################
#                  Pruebas para EstacionamientoReserva
###################################################################

class EstacionamientoReservaTestCase(TestCase):
	
	# malicia
	def test_EstacionamientoReserva_Vacio(self):
		form_data = {}
		form = EstacionamientoReserva(data = form_data)
		self.assertEqual(form.is_valid(), False)

	# caso borde
	def test_EstacionamientoReserva_UnCampo(self):
		form_data = {'inicio':datetime.time(6, 0)}
		form = EstacionamientoReserva(data = form_data)
		self.assertEqual(form.is_valid(), False)

	# normal
	def test_EstacionamientoReserva_TodosCamposBien(self):
		form_data = {'fechaInicio': datetime.date(2015,10,5),'horaInicio':datetime.time(6, 0),'fechaFinal': datetime.date(2015,10,5), 'horaFinal':datetime.time(12, 0)}
		form = EstacionamientoReserva(data = form_data)
		self.assertEqual(form.is_valid(), True)

	# malicia
	def test_EstacionamientoReserva_InicioString(self):
		form_data = {'inicio':'hola',
								'final':datetime.time(12, 0)}
		form = EstacionamientoReserva(data = form_data)
		self.assertEqual(form.is_valid(), False)

	# malicia
	def test_EstacionamientoReserva_FinString(self):
		form_data = {'inicio':datetime.time(6, 0),
								'final':'hola'}
		form = EstacionamientoReserva(data = form_data)
		self.assertEqual(form.is_valid(), False)

	# malicia
	def test_EstacionamientoReserva_InicioNone(self):
		form_data = {'inicio':None,
								'final':datetime.time(12, 0)}
		form = EstacionamientoReserva(data = form_data)
		self.assertEqual(form.is_valid(), False)

	# malicia
	def test_EstacionamientoReserva_FinalNone(self):
		form_data = {'inicio':datetime.time(6, 0),
								'final':None}
		form = EstacionamientoReserva(data = form_data)
		self.assertEqual(form.is_valid(), False)

##############################################################
# Estacionamiento Reserva Controlador
###################################################################

class EstacionamientoReservaControllerTestCase(TestCase):
# HorarioReserva, pruebas Unitarias

	# normal
	def test_HorarioReservaValido(self):
		ReservaInicio = datetime.datetime(2015,10,5,8,5)
		ReservaFin = datetime.datetime(2015,10,5,13,17)
		HoraApertura = datetime.time(hour = 8, minute = 0, second = 0)
		HoraCierre = datetime.time(hour = 18, minute = 0, second = 0)
		horaActual = datetime.datetime(2015,10,5,8,5)
		x = validarHorarioReserva(ReservaInicio, ReservaFin, HoraApertura, HoraCierre,horaActual)
		self.assertEqual(x, (True, ''))

	# caso borde
	def test_HorarioReservaInvalido_InicioReservacion_Mayor_FinalReservacion(self):
		ReservaInicio = datetime.datetime(year = 2015, month = 10, day = 5,hour = 13, minute = 0)
		ReservaFin = datetime.datetime(year = 2015, month = 10, day = 5,hour = 12, minute = 59)
		HoraApertura = datetime.time(hour = 12, minute = 0, second = 0)
		HoraCierre = datetime.time(hour = 18, minute = 0, second = 0)
		horaActual = datetime.datetime(year = 2015,month = 10, day = 5, hour = 12,minute = 50)
		x = validarHorarioReserva(ReservaInicio, ReservaFin, HoraApertura, HoraCierre,horaActual)
		self.assertEqual(x, (False, 'La hora de inicio de la reserva debe ser menor que la hora de fin de la reserva'))

	# caso borde
	def test_HorarioReservaInvalido_TiempoTotalMenor1h(self):
		ReservaInicio = datetime.datetime(year = 2015, month = 10, day = 5,hour = 13, minute = 0, second = 0)
		ReservaFin = datetime.datetime(year = 2015, month = 10, day = 5,hour = 13, minute = 59, second = 59)
		HoraApertura = datetime.time(hour = 12, minute = 0, second = 0)
		HoraCierre = datetime.time(hour = 18, minute = 0, second = 0)
		horaActual = datetime.datetime(year = 2015,month = 10, day = 5, hour = 12,minute = 50)
		x = validarHorarioReserva(ReservaInicio, ReservaFin, HoraApertura, HoraCierre,horaActual)
		self.assertEqual(x, (False, 'El tiempo de reserva debe ser al menos de 1 hora'))

	# caso borde
	def test_HorarioReservaInvalido_ReservaFinal_Mayor_HorarioCierre(self):
		ReservaInicio = datetime.datetime(year = 2015, month = 10, day = 5,hour = 13, minute = 0)
		ReservaFin = datetime.datetime(year = 2015, month = 10, day = 5,hour = 18, minute = 1)
		HoraApertura = datetime.time(hour = 12, minute = 0, second = 0)
		HoraCierre = datetime.time(hour = 18, minute = 0, second = 0)
		horaActual = datetime.datetime(year = 2015,month = 10, day = 5, hour = 12,minute = 50)
		x = validarHorarioReserva(ReservaInicio, ReservaFin, HoraApertura, HoraCierre,horaActual)
		self.assertEqual(x, (False, 'La hora de fin de la reserva debe estar en un horario valido'))

	# caso borde
	def test_HorarioReservaInvalido_ReservaInicial_Menor_HorarioApertura(self):
		ReservaInicio = datetime.datetime(year = 2015, month = 10, day = 5,hour = 11, minute = 59, second = 59)
		ReservaFin = datetime.datetime(year = 2015, month = 10, day = 5,hour = 15, minute = 0, second = 1)
		HoraApertura = datetime.time(hour = 12, minute = 0, second = 0)
		HoraCierre = datetime.time(hour = 18, minute = 0, second = 0)
		horaActual = datetime.datetime(year = 2015,month = 10, day = 5, hour = 12,minute = 50)
		x = validarHorarioReserva(ReservaInicio, ReservaFin, HoraApertura, HoraCierre, horaActual)
		self.assertEqual(x, (False, 'La hora de inicio de la reserva debe estar en un horario valido'))

		
###################################################################
#		Pruebas para validar horario pico
###################################################################

class ValidarHorarioPicoTestCase(TestCase):

	#normal
	def test_validarPicosHorarioPicoValido(self):

		horaPicoIni = datetime.time(12,0,0)
		horaPicoFin = datetime.time(14,0,0)
		inicioReservas = datetime.time(6,0,0)
		finReservas = datetime.time(18,0,0)
		tarifa = Decimal(20)
		tarifaPico = Decimal (30)
		
		respuesta = validarPicos(inicioReservas,finReservas,horaPicoIni,horaPicoFin,tarifa,tarifaPico)
		self.assertEqual(respuesta, (True, ''))
		
	#malicia	
	def test_validarPicosInicioHorarioPicoMayorFinHorarioPico(self):

		horaPicoIni = datetime.time(14,0,0)
		horaPicoFin = datetime.time(12,0,0)
		inicioReservas = datetime.time(6,0,0)
		finReservas = datetime.time(18,0,0)
		tarifa = Decimal(20)
		tarifaPico = Decimal (30)

		respuesta = validarPicos(inicioReservas,finReservas,horaPicoIni,horaPicoFin,tarifa,tarifaPico)
		self.assertEqual(respuesta, (False, 'La hora de inicio de la hora pico debe ser menor que el fin de la hora pico'))
	
	#malicia		
	def test_validarPicosTarifaPicoIgualTarifaValle(self):

		horaPicoIni = datetime.time(12,0,0)
		horaPicoFin = datetime.time(14,0,0)
		inicioReservas = datetime.time(6,0,0)
		finReservas = datetime.time(18,0,0)
		tarifa = Decimal(30)
		tarifaPico = Decimal (30)

		respuesta = validarPicos(inicioReservas,finReservas,horaPicoIni,horaPicoFin,tarifa,tarifaPico)
		self.assertEqual(respuesta, (False, 'La tarifa para el horario pico debe ser mayor que la tarifa para el horario valle'))
		
	#malicia
	def test_validarPicosInicioHorarioPicoMenorQueHorarioReservas(self):

		horaPicoIni = datetime.time(5,0,0)
		horaPicoFin = datetime.time(14,0,0)
		inicioReservas = datetime.time(6,0,0)
		finReservas = datetime.time(18,0,0)
		tarifa = Decimal(20)
		tarifaPico = Decimal (30)

		respuesta = validarPicos(inicioReservas,finReservas,horaPicoIni,horaPicoFin,tarifa,tarifaPico)
		self.assertEqual(respuesta, (False,'El horario pico debe estar dentro del horario de funcionamiento del estacionamiento'))
	
	#malicia
	def test_validarPicosFinHorarioPicoMayorQueHorarioReservas(self):

		horaPicoIni = datetime.time(12,0,0)
		horaPicoFin = datetime.time(19,0,0)
		inicioReservas = datetime.time(6,0,0)
		finReservas = datetime.time(18,0,0)
		tarifa = Decimal(20)
		tarifaPico = Decimal (30)

		respuesta = validarPicos(inicioReservas,finReservas,horaPicoIni,horaPicoFin,tarifa,tarifaPico)
		self.assertEqual(respuesta, (False,'El horario pico debe estar dentro del horario de funcionamiento del estacionamiento'))
	
	#malicia
	def test_validarPicosHorarioPicoIgualQueHorarioReservas(self):

		horaPicoIni = datetime.time(6,0,0)
		horaPicoFin = datetime.time(18,0,0)
		inicioReservas = datetime.time(6,0,0)
		finReservas = datetime.time(18,0,0)
		tarifa = Decimal(20)
		tarifaPico = Decimal (30)

		respuesta = validarPicos(inicioReservas,finReservas,horaPicoIni,horaPicoFin,tarifa,tarifaPico)
		self.assertEqual(respuesta, (False, 'Se debe garantizar la existencia de al menos un minuto de horario valle'))
	
	#malicia
	def test_validarPicosInicioHorarioPicoIgualFinHorarioPico(self):

		horaPicoIni = datetime.time(10,0,0)
		horaPicoFin = datetime.time(10,0,0)
		inicioReservas = datetime.time(6,0,0)
		finReservas = datetime.time(18,0,0)
		tarifa = Decimal(20)
		tarifaPico = Decimal (30)

		respuesta = validarPicos(inicioReservas,finReservas,horaPicoIni,horaPicoFin,tarifa,tarifaPico)
		self.assertEqual(respuesta, (False, 'La hora de inicio de la hora pico debe ser menor que el fin de la hora pico'))


#################################################################
#		Pruebas de Marzullo
################################################################

class MarzulloTestCase(TestCase):
	
	# caso borde
	def test_Reservar_horarios_todoeldia(self):
		Hora1In = datetime.datetime(year = 2015,month = 10,day = 5,hour = 6, minute = 0, second = 0)
		Hora1Out = datetime.datetime(year = 2015,month = 10,day = 5,hour = 6, minute = 0, second = 0)
		Hora2In = datetime.datetime(year = 2015,month = 10,day = 5,hour = 18, minute = 0, second = 0)
		Hora2Out = datetime.datetime(year = 2015,month = 10,day = 5,hour = 18, minute = 0, second = 0)
		lista = []
		lista.append([Hora1In, -1])
		lista.append([Hora1Out, 1])
		lista.append([Hora2In, -1])
		lista.append([Hora2Out, 1])
		HoraIn = datetime.datetime(year = 2015,month = 10,day = 5,hour = 6, minute = 0, second = 0)
		HoraOut = datetime.datetime(year = 2015,month = 10,day = 5,hour = 18, minute = 0, second = 0)
		x = reservar(HoraIn, HoraOut, lista,3)
		self.assertEqual(x, True)

	# caso borde
	def test_Reservar_noDisponible(self):
		Hora1In = datetime.datetime(year = 2015,month = 10,day = 5,hour = 6, minute = 0, second = 0)
		Hora1Out = datetime.datetime(year = 2015,month = 10,day = 5,hour = 18, minute = 0, second = 0)
		Hora2In = datetime.datetime(year = 2015,month = 10,day = 5,hour = 6, minute = 0, second = 0)
		Hora2Out = datetime.datetime(year = 2015,month = 10,day = 5,hour = 18, minute = 0, second = 0)
		Hora3In = datetime.datetime(year = 2015,month = 10,day = 5,hour = 6, minute = 0, second = 0)
		Hora3Out = datetime.datetime(year = 2015,month = 10,day = 5,hour = 18, minute = 0, second = 0)
		lista = []
		lista.append([Hora1In, -1])
		lista.append([Hora1Out, 1])
		lista.append([Hora3In, -1])
		lista.append([Hora3Out, 1])
		lista.append([Hora2In, -1])
		lista.append([Hora2Out, 1])
		HoraIn = datetime.datetime(year = 2015,month = 10,day = 5,hour = 7, minute = 0, second = 0)
		HoraOut = datetime.datetime(year = 2015,month = 10,day = 5,hour = 9, minute = 0, second = 0)
		x = reservar(HoraIn, HoraOut, lista,3)
		self.assertEqual(x,False)

	# normal
	def test_Reservar_noDisponible_reservarTodoElDia(self):
		Hora1In = datetime.datetime(year = 2015,month = 10,day = 5,hour = 6, minute = 0, second = 0)
		Hora1Out = datetime.datetime(year = 2015,month = 10,day = 5,hour = 18, minute = 0, second = 0)
		Hora2In = datetime.datetime(year = 2015,month = 10,day = 5,hour = 6, minute = 0, second = 0)
		Hora2Out = datetime.datetime(year = 2015,month = 10,day = 5,hour = 18, minute = 0, second = 0)
		Hora3In = datetime.datetime(year = 2015,month = 10,day = 5,hour = 6, minute = 0, second = 0)
		Hora3Out = datetime.datetime(year = 2015,month = 10,day = 5,hour = 18, minute = 0, second = 0)
		lista = []
		lista.append([Hora1In, -1])
		lista.append([Hora1Out, 1])
		lista.append([Hora3In, -1])
		lista.append([Hora3Out, 1])
		lista.append([Hora2In, -1])
		lista.append([Hora2Out, 1])
		HoraIn = datetime.datetime(year = 2015,month = 10,day = 5,hour = 6, minute = 0, second = 0)
		HoraOut = datetime.datetime(year = 2015,month = 10,day = 5,hour = 18, minute = 0, second = 0)
		x = reservar(HoraIn, HoraOut, lista, 3)
		self.assertEqual(x,False)

	# caso borde
	def test_Reservar_lista_solo_maxmin(self):
		Hora1In = datetime.datetime(year = 2015,month = 10,day = 5,hour = 6, minute = 0, second = 0)
		Hora1Out = datetime.datetime(year = 2015,month = 10,day = 5,hour = 6, minute = 0, second = 0)
		Hora2In = datetime.datetime(year = 2015,month = 10,day = 5,hour = 18, minute = 0, second = 0)
		Hora2Out = datetime.datetime(year = 2015,month = 10,day = 5,hour = 18, minute = 0, second = 0)
		lista = []
		lista.append([Hora1In, -1])
		lista.append([Hora1Out, 1])
		lista.append([Hora2In, -1])
		lista.append([Hora2Out, 1])
		HoraIn = datetime.datetime(year = 2015,month = 10,day = 5,hour = 12, minute = 0, second = 0)
		HoraOut = datetime.datetime(year = 2015,month = 10,day = 5,hour = 18, minute = 0, second = 0)
		x = reservar(HoraIn, HoraOut, lista, 3)
		self.assertEqual(x,True)
	

	# normal
	def test_Reservar_funcionalidadOK(self):
		Hora1In = datetime.datetime(year = 2015,month = 10,day = 5,hour = 6, minute = 0, second = 0)
		Hora1Out = datetime.datetime(year = 2015,month = 10,day = 5,hour = 6, minute = 0, second = 0)
		Hora2In = datetime.datetime(year = 2015,month = 10,day = 5,hour = 18, minute = 0, second = 0)
		Hora2Out = datetime.datetime(year = 2015,month = 10,day = 5,hour = 18, minute = 0, second = 0)
		lista = []
		lista.append([Hora1In, -1])
		lista.append([Hora1Out, 1])
		lista.append([Hora2In, -1])
		lista.append([Hora2Out, 1])
		estacionamiento = lista
		HoraIn = datetime.datetime(year = 2015,month = 10,day = 5,hour = 6, minute = 0, second = 0)
		HoraOut = datetime.datetime(year = 2015,month = 10,day = 5,hour = 12, minute = 0, second = 0)
		x = reservar(HoraIn, HoraOut, estacionamiento, 2)
		self.assertEqual(x,True)

	

# insertarReserva, Pruebas Unitarias
# no se requiere unas pruebas exaustivas de esta funcion, ya que esta funcion
# solo agrega una tupla a la lista otorgada utilizando la funcion 'insert' de las listas
# de python, la cual presumo que ha sido probada en gran cantidad de oportunidades

	# normal
	def test_Reservar_horas_Iguales(self):
		Hora1In = datetime.datetime(year = 2015,month = 10,day = 5,hour = 6, minute = 0, second = 0)
		Hora1Out = datetime.datetime(year = 2015,month = 10,day = 5,hour = 6, minute = 0, second = 0)
		Hora2In = datetime.datetime(year = 2015,month = 10,day = 5,hour = 18, minute = 0, second = 0)
		Hora2Out = datetime.datetime(year = 2015,month = 10,day = 5,hour = 18, minute = 0, second = 0)
		lista = []
		lista.append([Hora1In, -1])
		lista.append([Hora1Out, 1])
		lista.append([Hora2In, -1])
		lista.append([Hora2Out, 1])
		estacionamiento = lista
		HoraIn = datetime.datetime(year = 2015,month = 10,day = 5,hour = 6, minute = 0, second = 0)
		HoraOut = datetime.datetime(year = 2015,month = 10,day = 5,hour = 7, minute = 0, second = 0)
		x = reservar(HoraIn, HoraOut, estacionamiento, 2)
		self.assertEqual(x,True)

	# normal
	def test_reservar_funcionalidadOk(self):
		Hora1In = datetime.datetime(year = 2015,month = 10,day = 5,hour = 6, minute = 0, second = 0)
		Hora1Out = datetime.datetime(year = 2015,month = 10,day = 5,hour = 6, minute = 0, second = 0)
		Hora3In = datetime.datetime(year = 2015,month = 10,day = 5,hour = 8, minute = 0, second = 0)
		Hora3Out = datetime.datetime(year = 2015,month = 10,day = 5,hour = 12, minute = 0, second = 0)
		Hora2In = datetime.datetime(year = 2015,month = 10,day = 5,hour = 22, minute = 0, second = 0)
		Hora2Out = datetime.datetime(year = 2015,month = 10,day = 5,hour = 22, minute = 0, second = 0)
		lista = []
		lista.append([Hora1In, -1])
		lista.append([Hora1Out, 1])
		lista.append([Hora2In, -1])
		lista.append([Hora2Out, 1])
		x = reservar(Hora3In, Hora3Out, lista, 2)
		self.assertEqual(x, True)

#################################################################
# Pruebas para PagoReserva
#################################################################

class PagoReservaTestCase(TestCase):
	
    # frontera
	def test_PagoReserva_CamposBien(self):
		form_data = { 	'nombre' : 'Juan',
						'apellidos' : 'Perez',
						'nacionalidad' : 'E-',
						'cedula' : '12654378',
						'tipoTarjeta' : 'Xpres',
						'numTarjeta': '1234-1234-1234-1234',
							}
		form = PagoReserva(data = form_data)
		self.assertEqual(form.is_valid(), True)
	
    # frontera		
	def test_PagoReserva_TarjetaMayor16Digitos(self):
		form_data = { 	'nombre' : 'Juan',
						'apellidos' : 'Perez',
						'nacionalidad' : 'E-',
						'cedula' : '12654378',
						'numTarjeta': '1234-1234-1234-12345',
							}
		form = PagoReserva(data = form_data)
		self.assertEqual(form.is_valid(), False)
	
    # frontera
	def test_PagoReserva_TarjetaMenor16Digitos(self):
		form_data = { 	'nombre' : 'Juan',
						'apellidos' : 'Perez',
						'nacionalidad' : 'E-',
						'cedula' : '12654378',
						'numTarjeta': '1234-1234-1234-123',
							}
		form = PagoReserva(data = form_data)
		self.assertEqual(form.is_valid(), False)
	
    # malicia	
	def test_PagoReserva_SinTipo(self):
		form_data = { 	'nombre' : 'Juan',
						'apellidos' : 'Perez',
						'nacionalidad' : 'E-',
						'cedula' : '12654378',
						'numTarjeta': '1234-1234-1234-1234',
							}
		form = PagoReserva(data = form_data)
		self.assertEqual(form.is_valid(), False)
	
    # malicia
	def test_PagoReserva_NumTarjetaSinGuiones(self):
		form_data = { 	'nombre' : 'Juan',
						'apellidos' : 'Perez',
						'nacionalidad' : 'E-',
						'cedula' : '12654378',
						'tipoTarjeta': 'Mister',
						'numTarjeta': '1234-1234-1234-1234',
							}
		form = PagoReserva(data = form_data)
		self.assertEqual(form.is_valid(), True)
    
    # malicia
	def test_PagoReserva_NumTarjetaConLetras(self):
		form_data = { 	'nombre' : 'Juan',
						'apellidos' : 'Perez',
						'nacionalidad' : 'E-',
						'cedula' : '12654378',
						'tipoTarjeta': 'Mister',
						'numTarjeta': '1234-1234-1234-abcd',
							}
		form = PagoReserva(data = form_data)
		self.assertEqual(form.is_valid(), False)
	
    # malicia
	def test_PagoReserva_SinNacionalidad(self):
		form_data = { 	'nombre' : 'Juan',
				'apellidos' : 'Perez',
				'cedula' : '12654378',
				'tipoTarjeta' : 'Xpres',
				'numTarjeta': '1234-1234-1234-1234',
					}
		form = PagoReserva(data = form_data)
		self.assertEqual(form.is_valid(), False)
	
    # malicia	
	def test_PagoReserva_DosApellidos(self):
		form_data = { 	'nombre' : 'Juan',
						'apellidos' : 'Perez Linares',
						'nacionalidad' : 'V-',
						'cedula' : '12654378',
						'tipoTarjeta' : 'Xpres',
						'numTarjeta': '1234-1234-1234-1234',
					}
		form = PagoReserva(data = form_data)
		self.assertEqual(form.is_valid(), True)
	
    # malicia
	def test_PagoReserva_CedulaConLetras(self):
		form_data = { 	'nombre' : 'Juan',
						'apellidos' : 'Perez',
						'nacionalidad' : 'V-',
						'cedula' : 'B12654378',
						'tipoTarjeta' : 'Xpres',
						'numTarjeta': '1234-1234-1234-1234',
					}
		form = PagoReserva(data = form_data)
		self.assertEqual(form.is_valid(), False)
    
    # malicia
	def test_PagoReserva_CedulaVacia(self):
		form_data = { 	'nombre' : 'Juan',
						'apellidos' : 'Perez',
						'nacionalidad' : 'V-',
						'cedula' : '',
						'tipoTarjeta' : 'Xpres',
						'numTarjeta': '1234-1234-1234-1234',
					}
		form = PagoReserva(data = form_data)
		self.assertEqual(form.is_valid(), False)
	
class PruebasParaEsquemasTarifarios(unittest.TestCase):
		
	global min_tarifa, max_tarifa, estacionamiento, esq15, esq20, esq30, esqmin, esqmax
	global esq15M,esq20M,esq30M,esqminM,esqmaxM,esq15HF,esq20HF,esq30HF,esqminHF,esqmaxHF
	global esq15D,esq20D,esq30D,esqminD,esqmaxD
	min_tarifa = Decimal(0)
	max_tarifa = Decimal(9999999.99)
	estacionamiento = Estacionamiento(Propietario="DUBI",Nombre="Patty",Direccion="Richard",Rif="J-123456789")
	esq15=Hora(Estacionamiento=estacionamiento,Tarifa=Decimal(15))
	esq20=Hora(Estacionamiento=estacionamiento,Tarifa=Decimal(20))
	esq30=Hora(Estacionamiento=estacionamiento,Tarifa=Decimal(30))
	esqmin=Hora(Estacionamiento=estacionamiento,Tarifa=Decimal(min_tarifa))
	esqmax=Hora(Estacionamiento=estacionamiento,Tarifa=Decimal(max_tarifa))
	esq15M=Minuto(Estacionamiento=estacionamiento,Tarifa=Decimal(15))
	esq20M=Minuto(Estacionamiento=estacionamiento,Tarifa=Decimal(20))
	esq30M=Minuto(Estacionamiento=estacionamiento,Tarifa=Decimal(30))
	esqminM=Minuto(Estacionamiento=estacionamiento,Tarifa=Decimal(min_tarifa))
	esqmaxM=Minuto(Estacionamiento=estacionamiento,Tarifa=Decimal(max_tarifa))
	esq15HF=HoraFraccion(Estacionamiento=estacionamiento,Tarifa=Decimal(15))
	esq20HF=HoraFraccion(Estacionamiento=estacionamiento,Tarifa=Decimal(20))
	esq30HF=HoraFraccion(Estacionamiento=estacionamiento,Tarifa=Decimal(30))
	esqminHF=HoraFraccion(Estacionamiento=estacionamiento,Tarifa=Decimal(min_tarifa))
	esqmaxHF=HoraFraccion(Estacionamiento=estacionamiento,Tarifa=Decimal(max_tarifa))
	
	
#################################################################
#		Pruebas calculo de tarifa por horas 
################################################################
	
	# El minimo tiempo de reserva es de 1 hora
	# El máximo tiempo de reserva es de 7 dias
		
	# Extremo
	def test_tarifaPorHoraMinTiempo(self):
		inires = datetime.datetime(2015,7,5,18,25,0,0)
		finres = datetime.datetime(2015,7,5,19,25,0,0)
		self.assertEqual(esq15.calcularMonto(inires, finres), Decimal(15))
		
	# Extremo 
	def test_tarifaPorHoraMaxTiempo(self):
		inires = datetime.datetime(2015,7,5,18,25,0,0)
		finres = datetime.datetime(2015,7,12,18,25,0,0)
		self.assertEqual(esq15.calcularMonto(inires, finres), Decimal(15*24*7))
	
	# Extremo
	def test_tarifaPorHoraFraccion1Min(self):
		inires = datetime.datetime(2015,7,5,18,25,0,0)
		finres = datetime.datetime(2015,7,5,19,26,0,0)
		self.assertEqual(esq20.calcularMonto(inires, finres), Decimal(20*2))
		
	# Extremo
	def test_tarifaPorHoraHorasExactasMismoDia(self):
		inires = datetime.datetime(2015,7,5,18,25,0,0)
		finres = datetime.datetime(2015,7,5,21,25,0,0)
		self.assertEqual(esq30.calcularMonto(inires, finres), Decimal(30*3))
	
	# Extremo
	def test_tarifaPorHoraHorasExactasDiferentesDia(self):
		inires = datetime.datetime(2015,7,5,18,25,0,0)
		finres = datetime.datetime(2015,7,8,18,25,0,0)
		self.assertEqual(esq30.calcularMonto(inires, finres), Decimal(72*30))
	
	# Extremo
	def test_tarifaPorHoraFraccion59Min(self):
		inires = datetime.datetime(2015,7,5,18,25,0,0)
		finres = datetime.datetime(2015,7,5,20,24,0,0)
		self.assertEqual(esq20.calcularMonto(inires, finres), Decimal(20*2))
		
	# Extremo
	def test_tarifaPorHora1MinMenosQueTiempoMaximo(self):
		inires = datetime.datetime(2015,7,5,18,25,0,0)
		finres = datetime.datetime(2015,7,12,18,24,0,0)
		self.assertEqual(esq20.calcularMonto(inires, finres), Decimal(7*24*20))
	
	# Extremo
	def test_tarifaPorHoraMinimaTarifa(self):
		inires = datetime.datetime(2015,7,5,18,25,0,0)
		finres = datetime.datetime(2015,7,6,15,0,0,0)
		self.assertEqual(esqmin.calcularMonto(inires, finres), Decimal(0))
		
	# Extremo
	def test_tarifaPorHoraMaximaTarifa(self):
		inires = datetime.datetime(2015,7,5,18,25,0,0)
		finres = datetime.datetime(2015,7,5,20,0,0,0)
		self.assertEqual(esqmax.calcularMonto(inires, finres), Decimal(9999999.99*2).quantize(Decimal(10)**-2))
	
	# Esquina	
	def test_tarifaPorHoraMaxTarifaMaxTiempo(self):
		inires = datetime.datetime(2015,7,5,18,25,0,0)
		finres = datetime.datetime(2015,7,12,18,25,0,0)
		self.assertEqual(esqmax.calcularMonto(inires, finres), Decimal(9999999.99*7*24).quantize(Decimal(10)**-2))
		
#################################################################
#		Pruebas calculo de tarifa por minutos 
#################################################################

	# El minimo tiempo de reserva es de 1 hora
	# El máximo tiempo de reserva es de 7 dias

	# Extremo
	def test_tarifaPorMinutoMinTiempo(self):
		inires = datetime.datetime(2015,7,5,18,25,0,0)
		finres = datetime.datetime(2015,7,5,19,25,0,0)
		self.assertEqual(esq15M.calcularMonto(inires, finres), Decimal(15))
		
	# Extremo 
	def test_tarifaPorMinutoMaxTiempo(self):
		inires = datetime.datetime(2015,7,5,18,25,0,0)
		finres = datetime.datetime(2015,7,12,18,25,0,0)
		self.assertEqual(esq15M.calcularMonto(inires, finres), Decimal(15*24*7).quantize(Decimal(10)**-2))
		
	# Extremo
	def test_tarifaPorMinutoFraccion1Min(self):
		inires = datetime.datetime(2015,7,5,18,25,0,0)
		finres = datetime.datetime(2015,7,5,20,26,0,0)
		self.assertEqual(esq20M.calcularMonto(inires, finres), Decimal(20*2 + 20/60).quantize(Decimal(10)**-2))
	
	# Extremo
	def test_tarifaPorMinutoFraccion59Min(self):
		inires = datetime.datetime(2015,7,5,18,25,0,0)
		finres = datetime.datetime(2015,7,5,22,24,0,0)
		self.assertEqual(esq20M.calcularMonto(inires, finres), Decimal(20*3 + 59 *(20/60)).quantize(Decimal(10)**-2))
	
	# Extremo
	def test_tarifaPorMinutoHorasExactasMismoDia(self):
		inires = datetime.datetime(2015,7,5,18,25,0,0)
		finres = datetime.datetime(2015,7,5,21,25,0,0)
		self.assertEqual(esq30M.calcularMonto(inires, finres), Decimal(30*3))
	
	# Extremo
	def test_tarifaPorMinutoHorasExactasDiferentesDia(self):
		inires = datetime.datetime(2015,7,5,18,25,0,0)
		finres = datetime.datetime(2015,7,8,18,25,0,0)
		self.assertEqual(esq30M.calcularMonto(inires, finres), Decimal(72*30))
		
	# Extremo
	def test_tarifaPorMinuto1MinMenosQueTiempoMaximo(self):
		inires = datetime.datetime(2015,7,5,18,25,0,0)
		finres = datetime.datetime(2015,7,12,18,24,0,0)
		self.assertEqual(esq20M.calcularMonto(inires, finres), Decimal(round(6*24*20 + 23*20 + 20/60*59,2)).quantize(Decimal(10)**-2))

	# Extremo
	def test_tarifaPorMinutoMinimaTarifa(self):
		inires = datetime.datetime(2015,7,5,18,25,0,0)
		finres = datetime.datetime(2015,7,6,15,0,0,0)
		self.assertEqual(esqminM.calcularMonto(inires, finres), Decimal(0))
	
	# Extremo
	def test_tarifaPorMinutoMaximaTarifa(self):
		inires = datetime.datetime(2015,7,5,18,25,0,0)
		finres = datetime.datetime(2015,7,5,20,0,0,0)
		self.assertEqual(esqmaxM.calcularMonto(inires, finres), Decimal(9999999.99+9999999.99/60*35).quantize(Decimal(10)**-2))
	
	# Esquina
	def test_tarifaPorMinutoMaxTarifaMaxTiempo(self):
		inires = datetime.datetime(2015,7,5,18,25,0,0)
		finres = datetime.datetime(2015,7,12,18,25,0,0)
		self.assertEqual(esqmaxM.calcularMonto(inires, finres), Decimal(9999999.99*7*24).quantize(Decimal(10)**-2))

#################################################################
#		Pruebas calculo de tarifa por hora y fracion
#################################################################

	# El minimo tiempo de reserva es de 1 hora
	# El máximo tiempo de reserva es de 7 dias

	# Extremo
	def test_tarifaPorHoraYFraccionMinTiempo(self):
		inires = datetime.datetime(2015,7,5,18,25,0,0)
		finres = datetime.datetime(2015,7,5,19,25,0,0)
		self.assertEqual(esq15HF.calcularMonto(inires, finres), Decimal(15))
			
	# Extremo 
	def test_tarifaPorHoraYFraccionMaxTiempo(self):
		inires = datetime.datetime(2015,7,5,18,25,0,0)
		finres = datetime.datetime(2015,7,12,18,25,0,0)
		self.assertEqual(esq15HF.calcularMonto(inires, finres), Decimal(15*24*7).quantize(Decimal(10)**-2))
		
	# Extremo
	def test_tarifaPorHoraYFraccionFraccion1Min(self):
		inires = datetime.datetime(2015,7,5,18,25,0,0)
		finres = datetime.datetime(2015,7,5,20,26,0,0)
		self.assertEqual(esq20HF.calcularMonto(inires, finres), Decimal(20*2 + 10).quantize(Decimal(10)**-2))
	
	#  Extremo
	def test_tarifaPorHoraYFraccionFraccion30Min(self):
		inires = datetime.datetime(2015,7,5,18,25,0,0)
		finres = datetime.datetime(2015,7,5,20,55,0,0)
		self.assertEqual(esq20HF.calcularMonto(inires, finres), Decimal(20*2 + 10).quantize(Decimal(10)**-2))
	
	# Extremo
	def test_tarifaPorHoraYFraccionFraccion31Min(self):
		inires = datetime.datetime(2015,7,5,18,25,0,0)
		finres = datetime.datetime(2015,7,5,20,56,0,0)
		self.assertEqual(esq20HF.calcularMonto(inires, finres), Decimal(20*2 + 20).quantize(Decimal(10)**-2))
	
	# Extremo
	def test_tarifaPorHoraYFraccionFraccion59Min(self):
		inires = datetime.datetime(2015,7,5,18,25,0,0)
		finres = datetime.datetime(2015,7,5,22,24,0,0)
		self.assertEqual(esq20HF.calcularMonto(inires, finres), Decimal(20*3 + 20).quantize(Decimal(10)**-2))
	
	# Extremo
	def test_tarifaPorHoraYFraccionHorasExactasMismoDia(self):
		inires = datetime.datetime(2015,7,5,18,25,0,0)
		finres = datetime.datetime(2015,7,5,21,25,0,0)
		self.assertEqual(esq30HF.calcularMonto(inires, finres), Decimal(30*3))
	
	# Extremo
	def test_tarifaPorHoraYFraccionHorasExactasDiferentesDia(self):
		inires = datetime.datetime(2015,7,5,18,25,0,0)
		finres = datetime.datetime(2015,7,8,18,25,0,0)
		self.assertEqual(esq30HF.calcularMonto(inires, finres), Decimal(72*30))
	
	# Extremo
	def test_tarifaPorHoraYFraccion1MinMenosQueTiempoMaximo(self):
		inires = datetime.datetime(2015,7,5,18,25,0,0)
		finres = datetime.datetime(2015,7,12,18,24,0,0)
		self.assertEqual(esq20HF.calcularMonto(inires, finres), Decimal(6*24*20 + 23*20 + 20).quantize(Decimal(10)**-2))

	# Extremo
	def test_tarifaPorHoraYFraccionMinimaTarifa(self):
		inires = datetime.datetime(2015,7,5,18,25,0,0)
		finres = datetime.datetime(2015,7,6,15,0,0,0)
		self.assertEqual(esqminHF.calcularMonto(inires, finres), Decimal(0))
		
	# Extremo
	def test_tarifaPorHoraYFraccionMaximaTarifa(self):
		inires = datetime.datetime(2015,7,5,18,25,0,0)
		finres = datetime.datetime(2015,7,5,20,0,0,0)
		self.assertEqual(esqmaxHF.calcularMonto(inires, finres), Decimal(9999999.99*2).quantize(Decimal(10)**-2))
		
	# Esquina
	def test_tarifaPorHoraYFraccionMaxTarifaMaxTiempo(self):
		inires = datetime.datetime(2015,7,5,18,25,0,0)
		finres = datetime.datetime(2015,7,12,18,25,0,0)
		self.assertEqual(esqmaxHF.calcularMonto(inires, finres), Decimal(9999999.99*7*24).quantize(Decimal(10)**-2))

#################################################################
#		Pruebas calculo de tarifa diferencido por hora
#################################################################

	# El minimo tiempo de reserva es de 1 hora
	# El máximo tiempo de reserva es de 7 dias
	# El mínimo tiempo del horario pico es de 1 minuto
	# El máximo tiempo del horario pico es de 24 horas
	
	# Extremo
	def test_tarifaDiferenciadoPorHoraMinTiempoFueraHoraPico(self):
		tarifa = Decimal(15)
		inires = datetime.datetime(2015,7,5,18,25,0,0)
		finres = datetime.datetime(2015,7,5,19,25,0,0)
		tarifapico = Decimal(20)
		iniciopico = datetime.time(12,0,0)
		finpico = datetime.time(15,0,0)
		esq=DifHora(Estacionamiento=estacionamiento,Tarifa=tarifa,PicoIni=iniciopico,PicoFin=finpico,TarifaPico=tarifapico)
		
		self.assertEqual(esq.calcularMonto(inires, finres), Decimal(15))
	
	# Extremo	
	def test_tarifaDiferenciadoPorHoraMinTiempoDentroHoraPico(self):
		tarifa = Decimal(15)
		inires = datetime.datetime(2015,7,5,18,25,0,0)
		finres = datetime.datetime(2015,7,5,19,25,0,0)
		tarifapico = Decimal(20)
		iniciopico = datetime.time(15,0,0)
		finpico = datetime.time(20,0,0)
		esq=DifHora(Estacionamiento=estacionamiento,Tarifa=tarifa,PicoIni=iniciopico,PicoFin=finpico,TarifaPico=tarifapico)
		
		self.assertEqual(esq.calcularMonto(inires, finres), Decimal(20))

	# Extremo
	def test_tarifaDiferenciadoPorHoraReserva1MinutoAntesDeTerminarHorarioPico(self):
		tarifa = 20	
		inires = datetime.datetime(2015,7,5,12,25,0,0)
		finres = datetime.datetime(2015,7,5,15,59,0,0)
		tarifapico = 25
		iniciopico = datetime.time(14,0,0)
		finpico = datetime.time(16,0,0)
		esq=DifHora(Estacionamiento=estacionamiento,Tarifa=tarifa,PicoIni=iniciopico,PicoFin=finpico,TarifaPico=tarifapico)
	
		self.assertEqual(esq.calcularMonto(inires, finres), Decimal(20+35*20/60+25+25*59/60).quantize(Decimal(10)**-2))
			
	#  Extremo
	def test_tarifaDiferenciadoPorHoraMaxTiempo(self):
		tarifa = Decimal(15)
		inires = datetime.datetime(2015,7,5,18,25,0,0)
		finres = datetime.datetime(2015,7,12,18,25,0,0)
		tarifapico = Decimal(20)
		iniciopico = datetime.time(15,0,0)
		finpico = datetime.time(20,0,0)
		esq=DifHora(Estacionamiento=estacionamiento,Tarifa=tarifa,PicoIni=iniciopico,PicoFin=finpico,TarifaPico=tarifapico)
		
		self.assertEqual(esq.calcularMonto(inires, finres), Decimal(5*20*7+19*15*7).quantize(Decimal(10)**-2))
		
	# Extremo
	def test_tarifaDiferenciadoPorHora1MinMenosQueTiempoMaximo(self):
		tarifa = Decimal(20)
		inires = datetime.datetime(2015,7,5,18,25,0,0)
		finres = datetime.datetime(2015,7,12,18,24,0,0)
		tarifapico = Decimal(25)
		iniciopico = datetime.time(15,0,0)
		finpico = datetime.time(20,0,0)
		esq=DifHora(Estacionamiento=estacionamiento,Tarifa=tarifa,PicoIni=iniciopico,PicoFin=finpico,TarifaPico=tarifapico)
		
		self.assertEqual(esq.calcularMonto(inires, finres), Decimal(5*25*7+19*20*7-25/60).quantize(Decimal(10)**-2))

	# Esquina
	def test_tarifaDiferenciadoPorHoraReservaIgualQueHoraPico(self):
		tarifa = Decimal(20)
		inires = datetime.datetime(2015,7,5,13,25,0,0)
		finres = datetime.datetime(2015,7,5,18,25,0,0)
		tarifapico = Decimal(25)
		iniciopico = datetime.time(13,25,0,0)
		finpico = datetime.time(18,25,0,0)
		esq=DifHora(Estacionamiento=estacionamiento,Tarifa=tarifa,PicoIni=iniciopico,PicoFin=finpico,TarifaPico=tarifapico)
		
		self.assertEqual(esq.calcularMonto(inires, finres), Decimal(25*5).quantize(Decimal(10)**-2))

	# Extremo		
	def test_tarifaDiferenciadoPorHoraMinimoTiempoDeHoraPico(self):
		tarifa = Decimal(20)
		inires = datetime.datetime(2015,7,5,12,25,0,0)
		finres = datetime.datetime(2015,7,5,16,0,0,0)
		tarifapico = Decimal(25)
		iniciopico = datetime.time(15,0,0)
		finpico = datetime.time(15,1,0)
		esq=DifHora(Estacionamiento=estacionamiento,Tarifa=tarifa,PicoIni=iniciopico,PicoFin=finpico,TarifaPico=tarifapico)
	
		self.assertEqual(esq.calcularMonto(inires, finres), Decimal(214*20/60+25/60).quantize(Decimal(10)**-2))

	# Extremo
	def test_tarifaDiferenciadoPorHoraMaximoTiempoDeHoraPico(self):
		tarifa = Decimal(20)
		inires = datetime.datetime(2015,7,5,12,25,0,0)
		finres = datetime.datetime(2015,7,5,16,0,0,0)
		tarifapico = Decimal(25)
		iniciopico = datetime.time(0,0,0)
		finpico = datetime.time(23,59,0)
		esq=DifHora(Estacionamiento=estacionamiento,Tarifa=tarifa,PicoIni=iniciopico,PicoFin=finpico,TarifaPico=tarifapico)
		
		self.assertEqual(esq.calcularMonto(inires, finres), Decimal(215*25/60).quantize(Decimal(10)**-2))

	# Esquina
	def test_tarifaDiferenciadoPorHoraMaxTiempoFueraDeHoraPicoSinLimitesIncluidos(self):
		tarifa = Decimal(20)
		inires = datetime.datetime(2015,7,5,20,1,0,0)
		finres = datetime.datetime(2015,7,6,14,59,0,0)
		tarifapico = Decimal(25)
		iniciopico = datetime.time(15,0,0)
		finpico = datetime.time(20,0,0)
		esq=DifHora(Estacionamiento=estacionamiento,Tarifa=tarifa,PicoIni=iniciopico,PicoFin=finpico,TarifaPico=tarifapico)
		
		self.assertEqual(esq.calcularMonto(inires, finres), Decimal(19*20-20/60*2).quantize(Decimal(10)**-2))
	
	# Esquina	
	def test_tarifaDiferenciadoPorHoraMaxTiempoFueraDeHoraPicoConLimitesIncluidos(self):
		tarifa = Decimal(20)
		inires = datetime.datetime(2015,7,5,20,0,0,0)
		finres = datetime.datetime(2015,7,6,15,0,0,0)
		tarifapico = Decimal(25)
		iniciopico = datetime.time(15,0,0)
		finpico = datetime.time(20,0,0)
		esq=DifHora(Estacionamiento=estacionamiento,Tarifa=tarifa,PicoIni=iniciopico,PicoFin=finpico,TarifaPico=tarifapico)
		self.assertEqual(esq.calcularMonto(inires, finres), Decimal(19*20).quantize(Decimal(10)**-2))	

	# Extremo
	def test_tarifaDiferenciadoPorHoraMinTarifaEnHorarioValle(self):
		tarifa = min_tarifa
		inires = datetime.datetime(2015,7,5,12,25,0,0)
		finres = datetime.datetime(2015,7,6,3,25,0,0)
		tarifapico = Decimal(30)
		iniciopico = datetime.time(14,0,0)
		finpico = datetime.time(16,0,0)
		esq=DifHora(Estacionamiento=estacionamiento,Tarifa=tarifa,PicoIni=iniciopico,PicoFin=finpico,TarifaPico=tarifapico)
		self.assertEqual(esq.calcularMonto(inires, finres), Decimal(30*2).quantize(Decimal(10)**-2))

	# Extremo	
	def test_tarifaDiferenciadoPorHoraMaxTarifaEnHorarioPico(self):
		tarifa = max_tarifa-Decimal(0.01)
		inires = datetime.datetime(2015,7,5,12,25,0,0)
		finres = datetime.datetime(2015,7,6,3,25,0,0)
		tarifapico = max_tarifa
		iniciopico = datetime.time(14,0,0)
		finpico = datetime.time(16,0,0)
		esq=DifHora(Estacionamiento=estacionamiento,Tarifa=tarifa,PicoIni=iniciopico,PicoFin=finpico,TarifaPico=tarifapico)
		self.assertEqual(esq.calcularMonto(inires, finres), Decimal(9999999.99*2+9999999.98*95/60+9999999.98*11+9999999.98*25/60).quantize(Decimal(10)**-2))

	# Esquina maliciosa
	def test_tarifaDiferenciadoPorHoraMaxTiempoDeHoraPicoMaximoTiempoReserva(self):
		tarifa = Decimal(20)
		inires = datetime.datetime(2015,7,5,12,25,0,0)
		finres = datetime.datetime(2015,7,12,12,25,0,0)
		tarifapico = Decimal(30)
		iniciopico = datetime.time(0,0,0)
		finpico = datetime.time(23,58,0)
		esq=DifHora(Estacionamiento=estacionamiento,Tarifa=tarifa,PicoIni=iniciopico,PicoFin=finpico,TarifaPico=tarifapico)
		self.assertEqual(esq.calcularMonto(inires, finres), Decimal(24*7*30-7*20/60).quantize(Decimal(10)**-2))

	# Malicia
	def test_tarifaDiferenciadoPorHoraMaxTiempoDeHoraPicoReservaIgualQueHoraPico(self):
		tarifa = Decimal(20)
		inires = datetime.datetime(2015,7,5,0,0,0,0)
		finres = datetime.datetime(2015,7,5,23,58,0,0)
		tarifapico = Decimal(30)
		iniciopico = datetime.time(0,0,0)
		finpico = datetime.time(23,58,0)
		esq=DifHora(Estacionamiento=estacionamiento,Tarifa=tarifa,PicoIni=iniciopico,PicoFin=finpico,TarifaPico=tarifapico)
		self.assertEqual(esq.calcularMonto(inires, finres), Decimal(24*30-2*30/60).quantize(Decimal(10)**-2))

	
##########################################################################################
#		Pruebas calculo de tarifa diferenciado por fin de semana (hora y fracción)
##########################################################################################
		
	#extremo
	def test_tarifaDiferenciadoPorFinDeSemanaEnDiaDeSemanaMinTiempo(self):
		tarifa = Decimal(20)
		inires = datetime.datetime(2015,7,6,7,0,0,0)
		finres = datetime.datetime(2015,7,6,8,0,0,0)
		tarifafin = Decimal(30)
		esq=DifFin(Estacionamiento=estacionamiento,Tarifa=tarifa,TarifaFin=tarifafin)
		res=esq.calcularMonto(inires, finres)
		self.assertEqual(res, Decimal(20).quantize(Decimal(10)**-2))
		
	#extremo	
	def test_tarifaDiferenciadoPorFinDeSemanaEnDiaDeFinDeSemanaHoraYMedia(self):
		tarifa = Decimal(20)
		inires = datetime.datetime(2015,7,5,7,0,0,0)
		finres = datetime.datetime(2015,7,5,8,30,0,0)
		tarifafin = Decimal(30)
		esq=DifFin(Estacionamiento=estacionamiento,Tarifa=tarifa,TarifaFin=tarifafin)
		res=esq.calcularMonto(inires, finres)
		self.assertEqual(res, Decimal(60).quantize(Decimal(10)**-2))
		
	#extremo
	def test_tarifaDiferenciadoPorFinDeSemanaDeViernesASabadoMinTiempo(self):
		tarifa = Decimal(20)
		inires = datetime.datetime(2015,7,3,23,30,0,0)
		finres = datetime.datetime(2015,7,4,0,30,0,0)
		tarifafin = Decimal(30)
		esq=DifFin(Estacionamiento=estacionamiento,Tarifa=tarifa,TarifaFin=tarifafin)
		res=esq.calcularMonto(inires, finres)
		self.assertEqual(res, Decimal(30).quantize(Decimal(10)**-2))
		
	#extremo
	def test_tarifaDiferenciadoPorFinDeSemanaDeViernesASabadoMinTiempoTarifaFinMayor(self):
		tarifa = Decimal(30)
		inires = datetime.datetime(2015,7,3,23,30,0,0)
		finres = datetime.datetime(2015,7,4,0,30,0,0)
		tarifafin = Decimal(20)
		esq=DifFin(Estacionamiento=estacionamiento,Tarifa=tarifa,TarifaFin=tarifafin)
		res=esq.calcularMonto(inires, finres)
		self.assertEqual(res, Decimal(30).quantize(Decimal(10)**-2))

	#extremo
	def test_tarifaDiferenciadoPorFinDeSemanaDeDomingoALunesHoraY1Minuto(self):
		tarifa = Decimal(20)
		inires = datetime.datetime(2015,7,5,23,30,0,0)
		finres = datetime.datetime(2015,7,6,0,31,0,0)
		tarifafin = Decimal(30)
		esq=DifFin(Estacionamiento=estacionamiento,Tarifa=tarifa,TarifaFin=tarifafin)
		res=esq.calcularMonto(inires, finres)
		self.assertEqual(res, Decimal(40).quantize(Decimal(10)**-2))

	#extremo
	def test_tarifaDiferenciadoPorFinDeSemanaDeDomingoALunesHoraY1MinutoTarifaFinMayor(self):
		tarifa = Decimal(30)
		inires = datetime.datetime(2015,7,5,23,30,0,0)
		finres = datetime.datetime(2015,7,6,0,31,0,0)
		tarifafin = Decimal(20)
		esq=DifFin(Estacionamiento=estacionamiento,Tarifa=tarifa,TarifaFin=tarifafin)
		res=esq.calcularMonto(inires, finres)
		self.assertEqual(res, Decimal(45).quantize(Decimal(10)**-2))
		
	#esquina	
	def test_tarifaDiferenciadoPorFinDeSemanaDeViernesAlPrimerMinutoDelSabado(self):
		tarifa = Decimal(20)
		inires = datetime.datetime(2015,7,3,23,0,0,0)
		finres = datetime.datetime(2015,7,4,0,1,0,0)
		tarifafin = Decimal(30)
		esq=DifFin(Estacionamiento=estacionamiento,Tarifa=tarifa,TarifaFin=tarifafin)
		res=esq.calcularMonto(inires, finres)
		self.assertEqual(res, Decimal(35).quantize(Decimal(10)**-2))	
		
	#esquina maliciosa
	def test_tarifaDiferenciadoPorFinDeSemanaDeViernesALaMedianocheDelSabado(self):
		tarifa = Decimal(20)
		inires = datetime.datetime(2015,7,3,23,0,0,0)
		finres = datetime.datetime(2015,7,4,0,0,0,0)
		tarifafin = Decimal(30)
		esq=DifFin(Estacionamiento=estacionamiento,Tarifa=tarifa,TarifaFin=tarifafin)
		res=esq.calcularMonto(inires, finres)
		self.assertEqual(res, Decimal(20).quantize(Decimal(10)**-2))
		
	#esquina	
	def test_tarifaDiferenciadoPorFinDeSemanaDelUltimoMinutoDelDomingoALunesHoraYFraccion(self):
		tarifa = Decimal(30)
		inires = datetime.datetime(2015,7,5,23,59,0,0)
		finres = datetime.datetime(2015,7,6,1,28,0,0)
		tarifafin = Decimal(20)
		esq=DifFin(Estacionamiento=estacionamiento,Tarifa=tarifa,TarifaFin=tarifafin)
		res=esq.calcularMonto(inires, finres)
		self.assertEqual(res, Decimal(45).quantize(Decimal(10)**-2))
		
	#esquina
	def test_tarifaDiferenciadoPorFinDeSemanaMaxTiempo(self):
		tarifa = Decimal(10)
		inires = datetime.datetime(2015,7,5,0,30,0,0)
		finres = datetime.datetime(2015,7,12,0,30,0,0)
		tarifafin = Decimal(20)
		esq=DifFin(Estacionamiento=estacionamiento,Tarifa=tarifa,TarifaFin=tarifafin)
		res=esq.calcularMonto(inires, finres)
		self.assertEqual(res, Decimal(10*24*4+10*23+20+20*24*2).quantize(Decimal(10)**-2))	
		
	#esquina maliciosa
	def test_tarifaDiferenciadoPorFinDeSemanaMaxTiempoDesde0(self):
		tarifa = Decimal(10)
		inires = datetime.datetime(2015,7,5,0,0,0,0)
		finres = datetime.datetime(2015,7,12,0,0,0,0)
		tarifafin = Decimal(20)
		esq=DifFin(Estacionamiento=estacionamiento,Tarifa=tarifa,TarifaFin=tarifafin)
		res=esq.calcularMonto(inires, finres)
		self.assertEqual(res, Decimal(10*24*4+10*24+20*24*2).quantize(Decimal(10)**-2))
		
	#esquina	
	def test_tarifaDiferenciadoPorFinDeSemanaMinTarifa(self):
		tarifa = Decimal(min_tarifa)
		inires = datetime.datetime(2015,7,6,17,0,0,0)
		finres = datetime.datetime(2015,7,6,18,0,0,0)
		tarifafin = Decimal(min_tarifa+Decimal(0.01))
		esq=DifFin(Estacionamiento=estacionamiento,Tarifa=tarifa,TarifaFin=tarifafin)
		res=esq.calcularMonto(inires, finres)
		self.assertEqual(res, Decimal(0).quantize(Decimal(10)**-2))
		
	#esquina
	def test_tarifaDiferenciadoPorFinDeSemanaMaxTarifaHoraY59Min(self):
		tarifa = Decimal(max_tarifa-Decimal(0.01))
		inires = datetime.datetime(2015,7,5,17,0,0,0)
		finres = datetime.datetime(2015,7,5,18,59,0,0)
		tarifafin = Decimal(max_tarifa)
		esq=DifFin(Estacionamiento=estacionamiento,Tarifa=tarifa,TarifaFin=tarifafin)
		res=esq.calcularMonto(inires, finres)
		self.assertEqual(res, Decimal(max_tarifa*2).quantize(Decimal(10)**-2))
		
	#esquina	
	def test_tarifaDiferenciadoPorFinDeSemanaMaxTiempoDiasDeSemana(self):
		tarifa = Decimal(20)
		inires = datetime.datetime(2015,7,6,0,0,0,0)
		finres = datetime.datetime(2015,7,10,23,59,0,0)
		tarifafin = Decimal(30)
		esq=DifFin(Estacionamiento=estacionamiento,Tarifa=tarifa,TarifaFin=tarifafin)
		res=esq.calcularMonto(inires, finres)
		self.assertEqual(res, Decimal(20*24*5).quantize(Decimal(10)**-2))
		
	#esquina
	def test_tarifaDiferenciadoPorFinDeSemanaMaxTiempoDiasDeFinDeSemana(self):
		tarifa = Decimal(20)
		inires = datetime.datetime(2015,7,11,0,0,0,0)
		finres = datetime.datetime(2015,7,12,23,59,0,0)
		tarifafin = Decimal(30)
		esq=DifFin(Estacionamiento=estacionamiento,Tarifa=tarifa,TarifaFin=tarifafin)
		res=esq.calcularMonto(inires, finres)
		self.assertEqual(res, Decimal(30*24*2).quantize(Decimal(10)**-2))

###################################################################
#		Pruebas diferencia entre Decimal y Float
###################################################################

class PruebasDecimalYFloat(unittest.TestCase):

	#normal (prueba de aceptación)
	def test_diferenciaEntreDecimalYFloat(self):
		tarifa = Decimal(0.5)
		inires = datetime.datetime(2015,7,12,10,0,0,0)
		finres = datetime.datetime(2015,7,12,15,21,0,0)
		esq=Minuto(Estacionamiento=estacionamiento,Tarifa=tarifa)
		res=esq.calcularMonto(inires, finres)
		
		def calcularMontoFloat(tarifa,iniR,finR):
			tarifa=float(tarifa)
			temp1 = (finR-iniR).days*24 + (finR - iniR).seconds//3600
			temp2 = (finR-iniR).days*24 + (finR - iniR).seconds/3600
			minextra = temp2 - temp1
			fraccion = tarifa*minextra
			return round(tarifa*temp1+fraccion,2)
			
		resFloat=calcularMontoFloat(tarifa,inires,finres)
		self.assertNotEqual(res,resFloat)
		
		
###################################################################
#		Pruebas para Verificacion de Calcular Tasa de Reserva
###################################################################

class PruebasCalcularTasaReserva(unittest.TestCase):

	# Frontera
	def test_calcularTasaReservaHorasSinReservas(self):
		tabla = []
		res = []
		Horaini = datetime.datetime(2015,7,5,6,0,0,0)
		Horafin = datetime.datetime(2015,7,5,18,0,0,0)
		for i in range(0,8):
			res.append([0,0,0,0,0,0,0,0,0,0,0,0])
		estad = calcularTasaReservaHoras(tabla,Horaini,Horafin,3,Horaini)
		self.assertEqual(res,estad)
	
	# Frontera	
	def test_calcularTasaReservaHorasLleno(self):
		tabla = []
		res = []
		for i in range(0,3):
			tabla.append([datetime.datetime(2015,7,5,6,0,0,0),-1])
			tabla.append([datetime.datetime(2015,7,5,18,0,0,0),1])
		Horaini = datetime.datetime(2015,7,5,6,0,0,0)
		Horafin = datetime.datetime(2015,7,5,18,0,0,0)
		res.append([Decimal('99.9'),Decimal('99.9'),Decimal('99.9'),Decimal('99.9'),Decimal('99.9'),Decimal('99.9'),Decimal('99.9'),Decimal('99.9'),Decimal('99.9'),Decimal('99.9'),Decimal('99.9'),Decimal('99.9')])
		for i in range(0,7):
			res.append([0,0,0,0,0,0,0,0,0,0,0,0])
		estad = calcularTasaReservaHoras(tabla,Horaini,Horafin,3,Horaini)
		self.assertEqual(res,estad)
		
	# Frontera	
	def test_calcularTasaReservaReservaMinimaMasUnosMinutos(self):
		tabla = []
		res = []
		tabla.append([datetime.datetime(2015,7,5,6,0,0,0),-1])
		tabla.append([datetime.datetime(2015,7,5,7,1,0,0),1])
		Horaini = datetime.datetime(2015,7,5,6,0,0,0)
		Horafin = datetime.datetime(2015,7,5,18,0,0,0)
		res.append([Decimal('33.3'),Decimal('0.6'),0,0,0,0,0,0,0,0,0,0])
		for i in range(0,7):
			res.append([0,0,0,0,0,0,0,0,0,0,0,0])
		estad = calcularTasaReservaHoras(tabla,Horaini,Horafin,3,Horaini)
		self.assertEqual(res,estad)
		
	# Esquina	
	def test_calcularTasaReservaEstminimo(self):
		tabla = []
		res = []
		tabla.append([datetime.datetime(2015,7,5,6,0,0,0),-1])
		tabla.append([datetime.datetime(2015,7,5,7,0,0,0),1])
		tabla.append([datetime.datetime(2015,7,5,6,0,0,0),-1])
		tabla.append([datetime.datetime(2015,7,5,7,0,0,0),1])
		tabla.append([datetime.datetime(2015,7,5,6,0,0,0),-1])
		tabla.append([datetime.datetime(2015,7,5,7,0,0,0),1])
		Horaini = datetime.datetime(2015,7,5,6,0,0,0)
		Horafin = datetime.datetime(2015,7,5,7,0,0,0)
		res.append([Decimal('99.9')])
		for i in range(0,7):
			res.append([0])
		estad = calcularTasaReservaHoras(tabla,Horaini,Horafin,3,Horaini)
		self.assertEqual(res,estad)	
	
	# Frontera		
	def test_calcularTasaReservaEstmaximo(self):
		tabla = []
		res = []
		tabla.append([datetime.datetime(2015,7,5,0,0,0,0),-1])
		tabla.append([datetime.datetime(2015,7,5,23,59,0,0),1])
		tabla.append([datetime.datetime(2015,7,5,0,0,0,0),-1])
		tabla.append([datetime.datetime(2015,7,5,23,59,0,0),1])
		tabla.append([datetime.datetime(2015,7,5,0,0,0,0),-1])
		tabla.append([datetime.datetime(2015,7,5,23,59,0,0),1])
		Horaini = datetime.datetime(2015,7,5,0,0,0,0)
		Horafin = datetime.datetime(2015,7,5,23,59,0,0)
		res.append([Decimal('99.9'),Decimal('99.9'),Decimal('99.9'),Decimal('99.9'),Decimal('99.9'),Decimal('99.9'),
				Decimal('99.9'),Decimal('99.9'),Decimal('99.9'),Decimal('99.9'),Decimal('99.9'),Decimal('99.9'),
				Decimal('99.9'),Decimal('99.9'),Decimal('99.9'),Decimal('99.9'),Decimal('99.9'),Decimal('99.9'),
				Decimal('99.9'),Decimal('99.9'),Decimal('99.9'),Decimal('99.9'),Decimal('99.9'),Decimal('98.4')])
		for i in range(0,7):
			res.append([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0])
		estad = calcularTasaReservaHoras(tabla,Horaini,Horafin,3,Horaini)
		self.assertEqual(res,estad)
	
	# Malicia	
	def test_calcularTasaReservaLlenarhoraahora(self):	
		tabla = []
		res = []
		tabla.append([datetime.datetime(2015,7,5,0,0,0,0),-1])
		tabla.append([datetime.datetime(2015,7,5,1,0,0,0),1])
		tabla.append([datetime.datetime(2015,7,5,1,0,0,0),-1])
		tabla.append([datetime.datetime(2015,7,5,2,0,0,0),1])
		tabla.append([datetime.datetime(2015,7,5,2,0,0,0),-1])
		tabla.append([datetime.datetime(2015,7,5,3,0,0,0),1])
		tabla.append([datetime.datetime(2015,7,5,3,0,0,0),-1])
		tabla.append([datetime.datetime(2015,7,5,4,0,0,0),1])
		tabla.append([datetime.datetime(2015,7,5,4,0,0,0),-1])
		tabla.append([datetime.datetime(2015,7,5,5,0,0,0),1])
		tabla.append([datetime.datetime(2015,7,5,5,0,0,0),-1])
		tabla.append([datetime.datetime(2015,7,5,6,0,0,0),1])
		tabla.append([datetime.datetime(2015,7,5,6,0,0,0),-1])
		tabla.append([datetime.datetime(2015,7,5,7,0,0,0),1])
		tabla.append([datetime.datetime(2015,7,5,7,0,0,0),-1])
		tabla.append([datetime.datetime(2015,7,5,8,0,0,0),1])
		tabla.append([datetime.datetime(2015,7,5,8,0,0,0),-1])
		tabla.append([datetime.datetime(2015,7,5,9,0,0,0),1])
		tabla.append([datetime.datetime(2015,7,5,9,0,0,0),-1])
		tabla.append([datetime.datetime(2015,7,5,10,0,0,0),1])
		tabla.append([datetime.datetime(2015,7,5,10,0,0,0),-1])
		tabla.append([datetime.datetime(2015,7,5,11,0,0,0),1])
		tabla.append([datetime.datetime(2015,7,5,11,0,0,0),-1])
		tabla.append([datetime.datetime(2015,7,5,12,0,0,0),1])
		Horaini = datetime.datetime(2015,7,5,0,0,0,0)
		Horafin = datetime.datetime(2015,7,5,12,0,0,0)
		res.append([Decimal('100.0'),Decimal('100.0'),Decimal('100.0'),Decimal('100.0'),Decimal('100.0'),Decimal('100.0'),
				Decimal('100.0'),Decimal('100.0'),Decimal('100.0'),Decimal('100.0'),Decimal('100.0'),Decimal('100.0')])
		for i in range(0,7):
			res.append([0,0,0,0,0,0,0,0,0,0,0,0])
		estad = calcularTasaReservaHoras(tabla,Horaini,Horafin,1,Horaini)
		self.assertEqual(res,estad)
		
	# Extremo			
	def test_calcularTasaReservaSolapar(self):
		tabla = []
		res = []
		tabla.append([datetime.datetime(2015,7,5,6,0,0,0),-1])
		tabla.append([datetime.datetime(2015,7,5,10,0,0,0),1])
		tabla.append([datetime.datetime(2015,7,5,7,0,0,0),-1])
		tabla.append([datetime.datetime(2015,7,5,9,0,0,0),1])
		tabla.append([datetime.datetime(2015,7,5,11,0,0,0),-1])
		tabla.append([datetime.datetime(2015,7,5,14,0,0,0),1])
		tabla.append([datetime.datetime(2015,7,5,12,0,0,0),-1])
		tabla.append([datetime.datetime(2015,7,5,13,0,0,0),1])
		tabla.append([datetime.datetime(2015,7,5,14,0,0,0),-1])
		tabla.append([datetime.datetime(2015,7,5,18,0,0,0),1])
		tabla.append([datetime.datetime(2015,7,5,11,0,0,0),-1])
		tabla.append([datetime.datetime(2015,7,5,15,0,0,0),1])
		tabla.append([datetime.datetime(2015,7,5,17,0,0,0),-1])
		tabla.append([datetime.datetime(2015,7,5,18,0,0,0),1])
		Horaini = datetime.datetime(2015,7,5,6,0,0,0)
		Horafin = datetime.datetime(2015,7,5,18,0,0,0)
		res.append([Decimal('33.3'),Decimal('66.6'),Decimal('66.6'),Decimal('33.3'),0,Decimal('66.6'),
				Decimal('99.9'),Decimal('66.6'),Decimal('66.6'),Decimal('33.3'),Decimal('33.3'),Decimal('66.6')])
		for i in range(0,7):
			res.append([0,0,0,0,0,0,0,0,0,0,0,0])
		estad = calcularTasaReservaHoras(tabla,Horaini,Horafin,3,Horaini)
		self.assertEqual(res,estad)
	
	# Malicia
	def test_calcularTasaReservaSolaparyFrontera(self):
		tabla = []
		res = []
		tabla.append([datetime.datetime(2015,7,5,6,0,0,0),-1])
		tabla.append([datetime.datetime(2015,7,5,10,0,0,0),1])
		tabla.append([datetime.datetime(2015,7,5,7,0,0,0),-1])
		tabla.append([datetime.datetime(2015,7,5,9,0,0,0),1])
		tabla.append([datetime.datetime(2015,7,5,11,0,0,0),-1])
		tabla.append([datetime.datetime(2015,7,5,14,0,0,0),1])
		tabla.append([datetime.datetime(2015,7,5,12,0,0,0),-1])
		tabla.append([datetime.datetime(2015,7,5,13,0,0,0),1])
		tabla.append([datetime.datetime(2015,7,5,14,0,0,0),-1])
		tabla.append([datetime.datetime(2015,7,5,18,0,0,0),1])
		tabla.append([datetime.datetime(2015,7,5,11,0,0,0),-1])
		tabla.append([datetime.datetime(2015,7,5,15,0,0,0),1])
		tabla.append([datetime.datetime(2015,7,5,17,0,0,0),-1])
		tabla.append([datetime.datetime(2015,7,5,18,0,0,0),1])
		tabla.append([datetime.datetime(2015,7,5,15,0,0,0),-1])
		tabla.append([datetime.datetime(2015,7,5,17,0,0,0),1])
		tabla.append([datetime.datetime(2015,7,5,14,0,0,0),-1])
		tabla.append([datetime.datetime(2015,7,5,15,0,0,0),1])
		tabla.append([datetime.datetime(2015,7,5,10,0,0,0),-1])
		tabla.append([datetime.datetime(2015,7,5,11,0,0,0),1])
		res.append([Decimal('33.3'),Decimal('66.6'),Decimal('66.6'),Decimal('33.3'),Decimal('33.3'),Decimal('66.6'),
				Decimal('99.9'),Decimal('66.6'),Decimal('99.9'),Decimal('66.6'),Decimal('66.6'),Decimal('66.6')])
		for i in range(0,7):
			res.append([0,0,0,0,0,0,0,0,0,0,0,0])
		Horaini = datetime.datetime(2015,7,5,6,0,0,0)
		Horafin = datetime.datetime(2015,7,5,18,0,0,0)
		estad = calcularTasaReservaHoras(tabla,Horaini,Horafin,3,Horaini)
		self.assertEqual(res,estad)
	
	# Frontera	
	def test_calcularTasaReservaDiferentediasActual(self):
		tabla = []
		res = []
		tabla.append([datetime.datetime(2015,7,6,6,0,0,0),-1])
		tabla.append([datetime.datetime(2015,7,6,10,0,0,0),1])
		tabla.append([datetime.datetime(2015,7,5,13,0,0,0),-1])
		tabla.append([datetime.datetime(2015,7,5,14,0,0,0),1])
		tabla.append([datetime.datetime(2015,7,7,15,0,0,0),-1])
		tabla.append([datetime.datetime(2015,7,7,18,0,0,0),1])
		tabla.append([datetime.datetime(2015,7,5,10,0,0,0),-1])
		tabla.append([datetime.datetime(2015,7,5,11,0,0,0),1])
		tabla.append([datetime.datetime(2015,7,6,10,0,0,0),-1])
		tabla.append([datetime.datetime(2015,7,6,14,0,0,0),1])
		tabla.append([datetime.datetime(2015,7,7,7,0,0,0),-1])
		tabla.append([datetime.datetime(2015,7,7,9,0,0,0),1])
		tabla.append([datetime.datetime(2015,7,7,15,0,0,0),-1])
		tabla.append([datetime.datetime(2015,7,7,16,0,0,0),1])
		tabla.append([datetime.datetime(2015,7,5,15,0,0,0),-1])
		tabla.append([datetime.datetime(2015,7,5,18,0,0,0),1])
		tabla.append([datetime.datetime(2015,7,5,6,0,0,0),-1])
		tabla.append([datetime.datetime(2015,7,5,9,0,0,0),1])
		tabla.append([datetime.datetime(2015,7,5,6,0,0,0),-1])
		tabla.append([datetime.datetime(2015,7,5,7,0,0,0),1])
		Horaini = datetime.datetime(2015,7,5,6,0,0,0)
		Horafin = datetime.datetime(2015,7,5,18,0,0,0)
		res.append([Decimal('100.0'),Decimal('50.0'),Decimal('50.0'),0,Decimal('50.0'),0,
				0,Decimal('50.0'),0,Decimal('50.0'),Decimal('50.0'),Decimal('50.0')])
		res.append([Decimal('50.0'),Decimal('50.0'),Decimal('50.0'),Decimal('50.0'),Decimal('50.0'),Decimal('50.0'),
				Decimal('50.0'),Decimal('50.0'),0,0,0,0])
		res.append([0,Decimal('50.0'),Decimal('50.0'),0,0,0,0,0,0,Decimal('100.0'),Decimal('50.0'),Decimal('50.0')])
		for i in range(0,5):
			res.append([0,0,0,0,0,0,0,0,0,0,0,0])
		estad = calcularTasaReservaHoras(tabla,Horaini,Horafin,2,Horaini)
		self.assertEqual(res,estad)
		
	# Extremo		
	def test_calcularTasaReservaDiferentediasDentrode7dias(self):
		tabla = []
		res = []
		tabla.append([datetime.datetime(2015,7,12,6,0,0,0),-1])
		tabla.append([datetime.datetime(2015,7,12,10,0,0,0),1])
		tabla.append([datetime.datetime(2015,7,5,13,0,0,0),-1])
		tabla.append([datetime.datetime(2015,7,5,14,0,0,0),1])
		tabla.append([datetime.datetime(2015,7,7,15,0,0,0),-1])
		tabla.append([datetime.datetime(2015,7,7,18,0,0,0),1])
		tabla.append([datetime.datetime(2015,7,5,10,0,0,0),-1])
		tabla.append([datetime.datetime(2015,7,5,11,0,0,0),1])
		tabla.append([datetime.datetime(2015,7,12,10,0,0,0),-1])
		tabla.append([datetime.datetime(2015,7,12,14,0,0,0),1])
		tabla.append([datetime.datetime(2015,7,12,7,0,0,0),-1])
		tabla.append([datetime.datetime(2015,7,12,9,0,0,0),1])
		tabla.append([datetime.datetime(2015,7,7,15,0,0,0),-1])
		tabla.append([datetime.datetime(2015,7,7,16,0,0,0),1])
		tabla.append([datetime.datetime(2015,7,12,15,0,0,0),-1])
		tabla.append([datetime.datetime(2015,7,12,18,0,0,0),1])
		tabla.append([datetime.datetime(2015,7,5,6,0,0,0),-1])
		tabla.append([datetime.datetime(2015,7,5,9,0,0,0),1])
		tabla.append([datetime.datetime(2015,7,12,6,0,0,0),-1])
		tabla.append([datetime.datetime(2015,7,12,7,0,0,0),1])
		Horaini = datetime.datetime(2015,7,5,6,0,0,0)
		Horafin = datetime.datetime(2015,7,5,18,0,0,0)
		res.append([Decimal('50.0'),Decimal('50.0'),Decimal('50.0'),0,Decimal('50.0'),0,0,
				Decimal('50.0'),0,0,0,0])
		res.append([0,0,0,0,0,0,0,0,0,0,0,0])
		res.append([0,0,0,0,0,0,0,0,0,Decimal('100.0'),Decimal('50.0'),Decimal('50.0')])
		for i in range(0,4):
			res.append([0,0,0,0,0,0,0,0,0,0,0,0])
		res.append([Decimal('100.0'),Decimal('100.0'),Decimal('100.0'),Decimal('50.0'),Decimal('50.0'),Decimal('50.0'),
				Decimal('50.0'),Decimal('50.0'),0,Decimal('50.0'),Decimal('50.0'),Decimal('50.0')])
		estad = calcularTasaReservaHoras(tabla,Horaini,Horafin,2,Horaini)
		self.assertEqual(res,estad)

	# Malicia
	def test_calcularTasaReservaComenzarEnUnaHoraConMinutos(self):
		tabla = []
		res = []
		tabla.append([datetime.datetime(2015,7,5,6,0,0,0),-1])
		tabla.append([datetime.datetime(2015,7,5,10,0,0,0),1])
		tabla.append([datetime.datetime(2015,7,5,13,0,0,0),-1])
		tabla.append([datetime.datetime(2015,7,5,14,0,0,0),1])
		tabla.append([datetime.datetime(2015,7,5,15,45,0,0),-1])
		tabla.append([datetime.datetime(2015,7,5,18,0,0,0),1])
		tabla.append([datetime.datetime(2015,7,5,10,30,0,0),-1])
		tabla.append([datetime.datetime(2015,7,5,11,30,0,0),1])
		res.append([Decimal('100.0'),Decimal('100.0'),Decimal('100.0'),Decimal('100.0'),Decimal('50.0'),
				Decimal('50.0'),0,Decimal('100.0'),0,Decimal('25.0'),Decimal('100.0'),Decimal('100.0')])
		for i in range(0,7):
			res.append([0,0,0,0,0,0,0,0,0,0,0,0])
		Horaini = datetime.datetime(2015,7,5,6,0,0,0)
		Horafin = datetime.datetime(2015,7,5,18,0,0,0)
		estad = calcularTasaReservaHoras(tabla,Horaini,Horafin,1,Horaini)
		
		self.assertEqual(res,estad)
		
	# Extremo		
	def test_calcularTasaReservaVariasReservasAbarcaVariosdias(self):
		tabla = []
		res = []
		tabla.append([datetime.datetime(2015,7,5,13,0,0,0),-1])
		tabla.append([datetime.datetime(2015,7,7,6,0,0,0),1])
		tabla.append([datetime.datetime(2015,7,7,13,0,0,0),-1])
		tabla.append([datetime.datetime(2015,7,9,14,0,0,0),1])
		tabla.append([datetime.datetime(2015,7,9,15,0,0,0),-1])
		tabla.append([datetime.datetime(2015,7,10,15,0,0,0),1])
		Horaini = datetime.datetime(2015,7,5,0,0,0,0)
		Horafin = datetime.datetime(2015,7,5,23,59,0,0)
		res.append([0,0,0,0,0,0,0,0,0,0,0,0,0,Decimal('50.0'),Decimal('50.0'),Decimal('50.0'),Decimal('50.0'),
				Decimal('50.0'),Decimal('50.0'),Decimal('50.0'),Decimal('50.0'),Decimal('50.0'),Decimal('50.0'),
				Decimal('50.0')])
		res.append([Decimal('50.0'),Decimal('50.0'),Decimal('50.0'),Decimal('50.0'),Decimal('50.0'),Decimal('50.0'),
				Decimal('50.0'),Decimal('50.0'),Decimal('50.0'),Decimal('50.0'),Decimal('50.0'),Decimal('50.0'),
				Decimal('50.0'),Decimal('50.0'),Decimal('50.0'),Decimal('50.0'),Decimal('50.0'),Decimal('50.0'),
				Decimal('50.0'),Decimal('50.0'),Decimal('50.0'),Decimal('50.0'),Decimal('50.0'),Decimal('50.0')])
		res.append([Decimal('50.0'),Decimal('50.0'),Decimal('50.0'),Decimal('50.0'),Decimal('50.0'),Decimal('50.0'),
				0,0,0,0,0,0,0,Decimal('50.0'),Decimal('50.0'),Decimal('50.0'),Decimal('50.0'),Decimal('50.0'),
				Decimal('50.0'),Decimal('50.0'),Decimal('50.0'),Decimal('50.0'),Decimal('50.0'),Decimal('50.0')])
		res.append([Decimal('50.0'),Decimal('50.0'),Decimal('50.0'),Decimal('50.0'),Decimal('50.0'),Decimal('50.0'),
				Decimal('50.0'),Decimal('50.0'),Decimal('50.0'),Decimal('50.0'),Decimal('50.0'),Decimal('50.0'),
				Decimal('50.0'),Decimal('50.0'),Decimal('50.0'),Decimal('50.0'),Decimal('50.0'),Decimal('50.0'),
				Decimal('50.0'),Decimal('50.0'),Decimal('50.0'),Decimal('50.0'),Decimal('50.0'),Decimal('50.0')])
		res.append([Decimal('50.0'),Decimal('50.0'),Decimal('50.0'),Decimal('50.0'),Decimal('50.0'),Decimal('50.0'),
				Decimal('50.0'),Decimal('50.0'),Decimal('50.0'),Decimal('50.0'),Decimal('50.0'),Decimal('50.0'),
				Decimal('50.0'),Decimal('50.0'),0,Decimal('50.0'),Decimal('50.0'),Decimal('50.0'),
				Decimal('50.0'),Decimal('50.0'),Decimal('50.0'),Decimal('50.0'),Decimal('50.0'),Decimal('50.0')])
		res.append([Decimal('50.0'),Decimal('50.0'),Decimal('50.0'),Decimal('50.0'),Decimal('50.0'),Decimal('50.0'),
				Decimal('50.0'),Decimal('50.0'),Decimal('50.0'),Decimal('50.0'),Decimal('50.0'),Decimal('50.0'),
				Decimal('50.0'),Decimal('50.0'),Decimal('50.0'),0,0,0,0,0,0,0,0,0])
		res.append([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0])
		res.append([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0])
		estad = calcularTasaReservaHoras(tabla,Horaini,Horafin,2,Horaini)
		self.assertEqual(res,estad)
		
	# Esquina maliciosa	
	def test_calcularTasaReservaVariasReservaAbarca7dias(self):

		tabla = []
		res = []
		tabla.append([datetime.datetime(2015,7,5,0,0,0,0),-1])
		tabla.append([datetime.datetime(2015,7,12,23,59,0,0),1])
		Horaini = datetime.datetime(2015,7,5,0,0,0,0)
		Horafin = datetime.datetime(2015,7,5,23,59,0,0)
		for i in range(0,7):
			res.append([Decimal('100.0'),Decimal('100.0'),Decimal('100.0'),Decimal('100.0'),Decimal('100.0'),Decimal('100.0'),
				Decimal('100.0'),Decimal('100.0'),Decimal('100.0'),Decimal('100.0'),Decimal('100.0'),Decimal('100.0'),
				Decimal('100.0'),Decimal('100.0'),Decimal('100.0'),Decimal('100.0'),Decimal('100.0'),Decimal('100.0'),
				Decimal('100.0'),Decimal('100.0'),Decimal('100.0'),Decimal('100.0'),Decimal('100.0'),Decimal('100.0')])
		res.append([Decimal('100.0'),Decimal('100.0'),Decimal('100.0'),Decimal('100.0'),Decimal('100.0'),Decimal('100.0'),
				Decimal('100.0'),Decimal('100.0'),Decimal('100.0'),Decimal('100.0'),Decimal('100.0'),Decimal('100.0'),
				Decimal('100.0'),Decimal('100.0'),Decimal('100.0'),Decimal('100.0'),Decimal('100.0'),Decimal('100.0'),
				Decimal('100.0'),Decimal('100.0'),Decimal('100.0'),Decimal('100.0'),Decimal('100.0'),Decimal('98.3')])
		estad = calcularTasaReservaHoras(tabla,Horaini,Horafin,1,Horaini)
		self.assertEqual(res,estad)

###################################################################
#		Pruebas para Verificar forma ConsultarIngresoForm
###################################################################

class TestCaseIngresoForm(unittest.TestCase):
	
	#borde
	def test_ConsultarIngresoFormValido(self):
		form_data = {
					'rif' : 'J-12345678-0'
					}
		form = ConsultarIngresoForm(data = form_data)
		self.assertEqual(form.is_valid(), True)
		
	#borde
	def test_ConsultarIngresoFormNoValidoPorfaltadecaracteres(self):
		form_data = {
					'rif' : 'J-1234'
					}
		form = ConsultarIngresoForm(data = form_data)
		self.assertEqual(form.is_valid(), False)
		
	#borde
	def test_ConsultarIngresoFormNoValidoPorcaracteresincorrecto(self):
		form_data = {
					'rif' : 'K-12345678-0'
					}
		form = ConsultarIngresoForm(data = form_data)
		self.assertEqual(form.is_valid(), False)
		
###################################################################
#		Pruebas para Verificar forma ConsultarIngresoForm
###################################################################

class TestCaseobtenerIngresos(unittest.TestCase):
	
	#esquina
	def test_obtenerIngresosSinEstacionamientos(self):
		Estacionamiento.objects.all().delete()
		ReservasModel.objects.all().delete()
		ReciboPagoModel.objects.all().delete()
		ingresos = obtenerIngresos('J-12345678-0')
		self.assertEqual(ingresos, []) 
		
	#borde
	def test_obtenerIngresosEstacionamientosNocoincideRif(self):
		Estacionamiento.objects.all().delete()
		ReservasModel.objects.all().delete()
		ReciboPagoModel.objects.all().delete()
		obj = Estacionamiento(
				Propietario = 'Pedro Perez',
				Nombre = 'EstacionamientoA',
                Direccion = 'El Hatillo',
                Rif = 'J-12345678-1')
		obj.save()
		ingresos = obtenerIngresos('J-12345678-0')
		self.assertEqual(ingresos, [])
	
	#borde	
	def test_obtenerIngresosEstacionamientosSinReservas(self):
		Estacionamiento.objects.all().delete()
		ReservasModel.objects.all().delete()
		ReciboPagoModel.objects.all().delete()
		obj = Estacionamiento(
				Propietario = 'Pedro Perez',
				Nombre = 'EstacionamientoA',
                Direccion = 'El Hatillo',
                Rif = 'J-12345678-0')
		obj.save()
		ingresos = obtenerIngresos('J-12345678-0')
		self.assertEqual(ingresos, [['EstacionamientoA',0]])
		
	#normal
	def test_obtenerIngresosEstacionamientosConVariasReservas(self):
		Estacionamiento.objects.all().delete()
		ReservasModel.objects.all().delete()
		ReciboPagoModel.objects.all().delete()
		obj = Estacionamiento(
				Propietario = 'Pedro Perez',
				Nombre = 'EstacionamientoA',
                Direccion = 'El Hatillo',
                Rif = 'J-12345678-0')
		obj.save()
		reserva = ReservasModel(
				Estacionamiento = obj,
                InicioReserva = '2015-08-12 06:00:00',
                FinalReserva = '2015-08-12 10:00:00')
		reserva.save()
		pago = ReciboPagoModel(
                numeroRecibo = '1',
                Reserva = reserva,
                cedula = 'Venezolana' + '12345678',
                fechaTransaccion = '2015-08-11 07:00:00',
                TipoTarjeta = 'Mister',
                MontoPago = Decimal(16).quantize(Decimal(10)**-2)
                )
		pago.save()
		reserva2 = ReservasModel(
				Estacionamiento = obj,
                InicioReserva = '2015-08-12 13:00:00',
                FinalReserva = '2015-08-12 15:00:00')
		reserva2.save()
		pago2 = ReciboPagoModel(
                numeroRecibo = '2',
                Reserva = reserva2,
                cedula = 'Venezolana' + '12345678',
                fechaTransaccion = '2015-08-11 07:00:00',
                TipoTarjeta = 'Mister',
                MontoPago = Decimal(8).quantize(Decimal(10)**-2)
                )
		pago2.save()
		ingresos = obtenerIngresos('J-12345678-0')
		self.assertEqual(ingresos, [['EstacionamientoA',Decimal('24.0')]])
		
	#normal
	def test_obtenerIngresosMultiplesEstacionamientosUnaSolaCoincidencia(self):
		Estacionamiento.objects.all().delete()
		ReservasModel.objects.all().delete()
		ReciboPagoModel.objects.all().delete()
		obj = Estacionamiento(
				Propietario = 'Pedro Perez',
				Nombre = 'EstacionamientoA',
                Direccion = 'El Hatillo',
                Rif = 'J-12345678-0')
		obj.save()
		obj2 = Estacionamiento(
				Propietario = 'Pedro Perez',
				Nombre = 'EstacionamientoB',
                Direccion = 'El Hatillo',
                Rif = 'J-12345678-1')
		obj2.save()
		obj3 = Estacionamiento(
				Propietario = 'Pedro Perez',
				Nombre = 'EstacionamientoC',
                Direccion = 'El Hatillo',
                Rif = 'J-12345678-1')
		obj3.save()
		reserva = ReservasModel(
				Estacionamiento = obj,
                InicioReserva = '2015-08-12 06:00:00',
                FinalReserva = '2015-08-12 10:00:00')
		reserva.save()
		pago = ReciboPagoModel(
                numeroRecibo = '1',
                Reserva = reserva,
                cedula = 'Venezolana' + '12345678',
                fechaTransaccion = '2015-08-11 07:00:00',
                TipoTarjeta = 'Mister',
                MontoPago = Decimal(16).quantize(Decimal(10)**-2)
                )
		pago.save()
		ingresos = obtenerIngresos('J-12345678-0')
		self.assertEqual(ingresos, [['EstacionamientoA',Decimal('16.0')]])
		
	#normal
	def test_obtenerIngresosMultiplesEstacionamientosTodosCoinciden(self):
		Estacionamiento.objects.all().delete()
		ReservasModel.objects.all().delete()
		ReciboPagoModel.objects.all().delete()
		obj = Estacionamiento(
				Propietario = 'Pedro Perez',
				Nombre = 'EstacionamientoA',
                Direccion = 'El Hatillo',
                Rif = 'J-12345678-0')
		obj.save()
		obj2 = Estacionamiento(
				Propietario = 'Pedro Perez',
				Nombre = 'EstacionamientoB',
                Direccion = 'El Hatillo',
                Rif = 'J-12345678-0')
		obj2.save()
		obj3 = Estacionamiento(
				Propietario = 'Pedro Perez',
				Nombre = 'EstacionamientoC',
                Direccion = 'El Hatillo',
                Rif = 'J-12345678-0')
		obj3.save()
		reserva = ReservasModel(
				Estacionamiento = obj,
                InicioReserva = '2015-08-12 06:00:00',
                FinalReserva = '2015-08-12 10:00:00')
		reserva.save()
		reserva2 = ReservasModel(
				Estacionamiento = obj2,
                InicioReserva = '2015-08-12 13:00:00',
                FinalReserva = '2015-08-12 18:00:00')
		reserva2.save()
		reserva3 = ReservasModel(
				Estacionamiento = obj3,
                InicioReserva = '2015-08-12 13:00:00',
                FinalReserva = '2015-08-12 18:00:00')
		reserva3.save()
		pago = ReciboPagoModel(
                numeroRecibo = '1',
                Reserva = reserva,
                cedula = 'Venezolana' + '12345678',
                fechaTransaccion = '2015-08-11 07:00:00',
                TipoTarjeta = 'Mister',
                MontoPago = Decimal(16).quantize(Decimal(10)**-2)
                )
		pago.save()
		pago2 = ReciboPagoModel(
                numeroRecibo = '2',
                Reserva = reserva2,
                cedula = 'Venezolana' + '12345678',
                fechaTransaccion = '2015-08-11 07:00:00',
                TipoTarjeta = 'Mister',
                MontoPago = Decimal(20).quantize(Decimal(10)**-2)
                )
		pago2.save()
		pago3 = ReciboPagoModel(
                numeroRecibo = '3',
                Reserva = reserva3,
                cedula = 'Venezolana' + '12345678',
                fechaTransaccion = '2015-08-11 07:00:00',
                TipoTarjeta = 'Mister',
                MontoPago = Decimal(27.5).quantize(Decimal(10)**-2)
                )
		pago3.save()
		ingresos = obtenerIngresos('J-12345678-0')
		self.assertEqual(ingresos, [['EstacionamientoA',Decimal('16.0')],
								['EstacionamientoB',Decimal('20.0')],
								['EstacionamientoC',Decimal('27.5')]])
		
	#borde
	def test_obtenerIngresosMultipleEstacionamientosNocoincideRif(self):
		Estacionamiento.objects.all().delete()
		ReservasModel.objects.all().delete()
		ReciboPagoModel.objects.all().delete()
		obj = Estacionamiento(
				Propietario = 'Pedro Perez',
				Nombre = 'EstacionamientoA',
                Direccion = 'El Hatillo',
                Rif = 'J-12345678-1')
		obj.save()
		obj2 = Estacionamiento(
				Propietario = 'Pedro Perez',
				Nombre = 'EstacionamientoB',
                Direccion = 'El Hatillo',
                Rif = 'J-12345678-1')
		obj2.save()
		obj3 = Estacionamiento(
				Propietario = 'Pedro Perez',
				Nombre = 'EstacionamientoC',
                Direccion = 'El Hatillo',
                Rif = 'J-12345678-5')
		obj3.save()
		obj4 = Estacionamiento(
				Propietario = 'Pedro Perez',
				Nombre = 'EstacionamientoD',
                Direccion = 'El Hatillo',
                Rif = 'J-12345678-4')
		obj4.save()
		obj5 = Estacionamiento(
				Propietario = 'Pedro Perez',
				Nombre = 'EstacionamientoE',
                Direccion = 'El Hatillo',
                Rif = 'J-12345678-4')
		obj5.save()
		ingresos = obtenerIngresos('J-12345678-0')
		self.assertEqual(ingresos, [])
	
	#esquina	
	def test_obtenerIngresosMaximoEstacionamientosTodosCoinciden(self):
		Estacionamiento.objects.all().delete()
		ReservasModel.objects.all().delete()
		ReciboPagoModel.objects.all().delete()
		obj = Estacionamiento(
				Propietario = 'Pedro Perez',
				Nombre = 'EstacionamientoA',
                Direccion = 'El Hatillo',
                Rif = 'J-12345678-0')
		obj.save()
		obj2 = Estacionamiento(
				Propietario = 'Pedro Perez',
				Nombre = 'EstacionamientoB',
                Direccion = 'El Hatillo',
                Rif = 'J-12345678-0')
		obj2.save()
		obj3 = Estacionamiento(
				Propietario = 'Pedro Perez',
				Nombre = 'EstacionamientoC',
                Direccion = 'El Hatillo',
                Rif = 'J-12345678-0')
		obj3.save()
		obj4 = Estacionamiento(
				Propietario = 'Pedro Perez',
				Nombre = 'EstacionamientoD',
                Direccion = 'El Hatillo',
                Rif = 'J-12345678-0')
		obj4.save()
		obj5 = Estacionamiento(
				Propietario = 'Pedro Perez',
				Nombre = 'EstacionamientoE',
                Direccion = 'El Hatillo',
                Rif = 'J-12345678-0')
		obj5.save()
		reserva = ReservasModel(
				Estacionamiento = obj,
                InicioReserva = '2015-08-12 06:00:00',
                FinalReserva = '2015-08-12 10:00:00')
		reserva.save()
		reserva2 = ReservasModel(
				Estacionamiento = obj2,
                InicioReserva = '2015-08-12 13:00:00',
                FinalReserva = '2015-08-12 18:00:00')
		reserva2.save()
		reserva3 = ReservasModel(
				Estacionamiento = obj3,
                InicioReserva = '2015-08-12 13:00:00',
                FinalReserva = '2015-08-12 18:00:00')
		reserva3.save()
		pago = ReciboPagoModel(
                numeroRecibo = '1',
                Reserva = reserva,
                cedula = 'Venezolana' + '12345678',
                fechaTransaccion = '2015-08-11 07:00:00',
                TipoTarjeta = 'Mister',
                MontoPago = Decimal(16).quantize(Decimal(10)**-2)
                )
		pago.save()
		pago2 = ReciboPagoModel(
                numeroRecibo = '2',
                Reserva = reserva2,
                cedula = 'Venezolana' + '12345678',
                fechaTransaccion = '2015-08-11 07:00:00',
                TipoTarjeta = 'Mister',
                MontoPago = Decimal(20).quantize(Decimal(10)**-2)
                )
		pago2.save()
		pago3 = ReciboPagoModel(
                numeroRecibo = '3',
                Reserva = reserva3,
                cedula = 'Venezolana' + '12345678',
                fechaTransaccion = '2015-08-11 07:00:00',
                TipoTarjeta = 'Mister',
                MontoPago = Decimal(27.5).quantize(Decimal(10)**-2)
                )
		pago3.save()
		ingresos = obtenerIngresos('J-12345678-0')
		self.assertEqual(ingresos, [['EstacionamientoA',Decimal('16.0')],
								['EstacionamientoB',Decimal('20.0')],
								['EstacionamientoC',Decimal('27.5')],
								['EstacionamientoD',0],
								['EstacionamientoE',0]])
		
class ConsultarReservasFormTestCase(TestCase):
	
    # frontera
	def test_consultarReservasCamposBien(self):
		form_data = { 	'nacionalidad' : 'V-',
						'cedula': '12345678',
						}
		form = ConsultarReservasForm(data = form_data)
		self.assertEqual(form.is_valid(), True)
	# Frontera	
	def test_consultarReservasErrorCedula(self):
		form_data = { 	'nacionalidad' : 'V-',
						'cedula': '123A5678',
						}
		form = ConsultarReservasForm(data = form_data)
		self.assertEqual(form.is_valid(), False)
	# Malicia	
	def test_consultarReservasSinNacionalidad(self):
		form_data = { 	'cedula': '12345678',
						}
		form = ConsultarReservasForm(data = form_data)
		self.assertEqual(form.is_valid(), False)