'''
27/01/2015

Jorge Marcano : 11-10566
Maria Victoria Jorge : 11-10566

'''

import unittest
from Estacionamiento import Estacionamiento

class TestReservar(unittest.TestCase):
    
    def testExistenciaFuncion(self):    # TDD puro.
        e = Estacionamiento(10)
        e.reservar(10,15)
          
    def testReservacionVacio(self): # TDD puro y frontera.
        e = Estacionamiento(10)
        e.reservaciones = []
        self.assertEquals(e.reservar(10,12),True)
          
    def testReservacionRechazada(self): # TDD puro y frontera.
        e = Estacionamiento(10)
        for i in range(0,e.puestos):
            e.reservaciones.append([10,-1])
            e.reservaciones.append([12,1])    
        self.assertEquals(e.reservar(10,12),False)
          
    def testUnaReservacionNoSolapada(self): # El estacionamiento tiene una reservacion y la nueva no la solapara
        e = Estacionamiento(10)
        e.reservaciones = [[10,-1],[14,1]]
        self.assertEquals(e.reservar(15,16),True)
      
    def testDiezReservacionesNoLleno(self): # TDD puro.
        e = Estacionamiento(10)
        e.reservaciones = [[8,-1],[9,1]]
        for i in range(0,e.puestos-1):
            e.reservaciones.append([10,-1])
            e.reservaciones.append([12,1])  
        self.assertEquals(e.reservar(14,16),True)
          
    def testReservacionSolapadaInterna(self): # TDD puro.
        e = Estacionamiento(10)
        for i in range(0,e.puestos):
            e.reservaciones.append([10,-1])
            e.reservaciones.append([15,1])    
        self.assertEquals(e.reservar(12,14),False)
            
    def testReservacionSolapadaExterna(self): # TDD puro.
        e = Estacionamiento(10)
        for i in range(0,e.puestos):
            e.reservaciones.append([12,-1])
            e.reservaciones.append([14,1])    
        self.assertEquals(e.reservar(10,16),False)
          
    def testReservacionSolapadaMixta(self): # TDD puro.
        e = Estacionamiento(10)
        for i in range(0,e.puestos):
            e.reservaciones.append([12,-1])
            e.reservaciones.append([14,1])    
        self.assertEquals(e.reservar(10,13),False)
          
    def testDosIntervalosMaximos(self): # TDD puro. (Malicia)
        e = Estacionamiento(10)
        for i in range(0,e.puestos):
            e.reservaciones.append([9,-1])
            e.reservaciones.append([10,1])
            e.reservaciones.append([14,-1])
            e.reservaciones.append([16,1])    
        self.assertEquals(e.reservar(14,16),False)
          
    def testEstacionamientoOcupadoDiaEntero(self): # Esquina
        e = Estacionamiento(10)
        for i in range(0,e.puestos-1):
            e.reservaciones.append([6,-1])
            e.reservaciones.append([18,1])    
        self.assertEquals(e.reservar(6,18),True)
          
    def testHoraInvalidaMinima(self): # TDD puro (condicion de entrada valida) y frontera.
        e = Estacionamiento(10)
        for i in range(0,e.puestos-4) :
            e.reservaciones.append([9,-1])
            e.reservaciones.append([12,1])
            e.reservaciones.append([6,-1])
            e.reservaciones.append([7,1])
              
        self.assertEquals(e.reservar(5,13),-1)
          
    def testHoraInvalidaMaxima(self): # TDD puro (condicion de entrada valida) y frontera.
        e = Estacionamiento(10)
        for i in range(0,e.puestos-4) :
            e.reservaciones.append([9,-1])
            e.reservaciones.append([12,1])
            e.reservaciones.append([6,-1])
            e.reservaciones.append([7,1])
              
        self.assertEquals(e.reservar(16,19),-1)
         
    def testDobleSolapamientoMaxima(self): # Caso malicioso
        e = Estacionamiento(10)
        for i in range(0,e.puestos//2) :
            e.reservaciones.append([11,-1])
            e.reservaciones.append([13,1])
            e.reservaciones.append([12,-1])
            e.reservaciones.append([14,1])
         
        self.assertEquals(e.reservar(12,13),False)
         
    def testReservacionInvalida(self): # TDD puro (condicion de entrada validad)
        e = Estacionamiento(10)
        for i in range(0,e.puestos) :
            e.reservaciones.append([12,-1])
            e.reservaciones.append([14,1])
     
        self.assertEquals(e.reservar(12,10),-1)
        
    def testReservacionesSeguidas(self): # Malicioso
        e = Estacionamiento(10)
        
        for i in range(0,3) :
            e.reservaciones.append([6,-1])
            e.reservaciones.append([7,1])
            e.reservaciones.append([10,-1])
            e.reservaciones.append([12,1])
            
        for i in range(0,e.puestos) : 
            e.reservaciones.append([12,-1])
            e.reservaciones.append([15,1])
            
        self.assertEquals(e.reservar(11,14),False)