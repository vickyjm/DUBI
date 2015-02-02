'''
Descripcion: Suite de pruebas unitarias de la Tarea 3.

@author: Monica Figuera 11-10328
@author: Enrique Iglesias 11-10477
'''

import unittest
from Taller3Est import *


class TestEst(unittest.TestCase):
    
    def testReservaciones(self):
        formato = '%H:%M'
        
        est = Estacionamiento(10)

        #Esquina: Primera reservacion. (Siguiendo orden TDD estricto)
        est.reservaciones = []    
        horaIni = datetime.strptime("06:00", formato)
        horaFin = datetime.strptime("09:00", formato)
        self.assertEqual(est.verificarDisponibilidad(horaIni.hour,horaFin.hour), True)
        
		#Frontera y esquina: Primera reservacion empezando en hora min. Tiempo minimo de reserva
        est.reservaciones = []    
        horaIni = datetime.strptime("06:00", formato)
        horaFin = datetime.strptime("07:00", formato)
        self.assertEqual(est.verificarDisponibilidad(horaIni.hour,horaFin.hour), True)

        #Frontera: Maximo de est.reservaciones posibles en un intervalo.
        est.reservaciones = [[6,9], [6,9], [6,9], [6,9], [6,9], [6,9], [6,9], [6,9], [6,9], [6,9]]
        horaIni = datetime.strptime("06:00", formato)
        horaFin = datetime.strptime("09:00", formato)
        self.assertEqual(est.verificarDisponibilidad(horaIni.hour,horaFin.hour), False)
        
        #Esquina: Tratar de realizar una reserva donde el intervalo esta lleno
        est.reservaciones =[[6,9],[6,9],[6,9],[6,9],[6,9],[6,9],[6,9],[6,9],[6,9],[6,9],
                   [9,10],[9,10],[9,10],[9,10],[9,10],[9,10],[9,10],[9,10],[9,10],[9,10]]
        horaIni = datetime.strptime("07:00", formato)
        horaFin = datetime.strptime("18:00", formato)
        self.assertEqual(est.verificarDisponibilidad(horaIni.hour,horaFin.hour), False)
        
        #Esquina: Tratar de realizar una reserva donde el intervalo esta lleno
        est.reservaciones =[[6,9],[6,9],[6,9],[6,9],[6,9],[6,9],[6,9],[6,9],[6,9],[6,9],
                   [9,10],[9,10],[9,10],[9,10],[9,10],[9,10],[9,10],[9,10],[9,10],[9,10]]
        horaIni = datetime.strptime("08:00", formato)
        horaFin = datetime.strptime("10:00", formato)
        self.assertEqual(est.verificarDisponibilidad(horaIni.hour,horaFin.hour), False)

        #Frontera y esquina: Tratar de realizar una reserva teniendo el estacionamiento lleno.
        est.reservaciones = [[6,18], [6,18], [6,18], [6,18], [6,18], [6,18], [6,18], [6,18], [6,18], [6,18]]
        horaIni = datetime.strptime("06:00", formato)
        horaFin = datetime.strptime("18:00", formato)
        self.assertEqual(est.verificarDisponibilidad(horaIni.hour,horaFin.hour), False)
        
        #Malicia: Comienzan unas est.reservaciones a las 13:00 y una nueva termina cuando empiezan estas. 
        est.reservaciones =[[12,14],[12,14],[12,14],[12,14],[12,14],[12,-1],[13,15],[13,15],[13,15],[13,15],[13,15]]
        horaIni = datetime.strptime("10:00", formato)
        horaFin = datetime.strptime("13:00", formato)
        self.assertEqual(est.verificarDisponibilidad(horaIni.hour,horaFin.hour), True)
        
        #Esquina: Ingresar reservacion hora minima despues de varias reservaciones
        #         que terminen en hora maxima. (Orden TDD estricto)
        est.reservaciones =[[6,9],[7,10],[8,11],[9,12],[10,13],[11,14],[12,15],[13,16],[14,17],[15,18]]
        horaIni = datetime.strptime("06:00", formato)
        horaFin = datetime.strptime("09:00", formato)
        self.assertEqual(est.verificarDisponibilidad(horaIni.hour,horaFin.hour), True)
        
        #Esquina, Frontera y Malicia: 10 carros reservan por la mitad del dia (06:00 - 12:00) y otros 
        #                            10 reservan por el resto del dia (12:00 - 18:00); luego otro carro trata
        #                            de reservar por una hora de 11:00 a 12:00. (Orden TDD escricto)
        est.reservaciones = [[6,12], [6,12], [6,12], [6,12], [6,12], [6,12], [6,12], [6,12], [6,12], [6,12],
                    [12,18], [12,18], [12,18], [12,18], [12,18], [12,18], [12,18], [12,18], [12,18], [12,18]]
        horaIni = datetime.strptime("11:00", formato)
        horaFin = datetime.strptime("12:00", formato)
        self.assertEqual(est.verificarDisponibilidad(horaIni.hour,horaFin.hour), False)