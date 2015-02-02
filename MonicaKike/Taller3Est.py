'''
Descripcion: Modulo principal de la Tarea 3.
Se implemento el algoritmo de Marzullo modificado, tomando en cuenta para el calculo solo
los intervalos contenidos en la nueva reservacion a agregar.
Se asumen los datos de entrada validos, los cuales se verifican mediante programacion defensiva
en el main de este modulo

@author: Monica Figuera 11-10328
@author: Enrique Iglesias 11-10477
'''

from datetime import datetime,timedelta

class Estacionamiento:
    def __init__(self,capacidad):
        self.__capacidad = capacidad
        self.__horaMinReserva = 6
        self.__horaMaxReserva = 18
        self.reservaciones = []
        
    def getCapacidad(self):
        return self.__capacidad

    def getHoraMinReserva(self):
        return self.__horaMinReserva

    def getHoraMaxReserva(self):
        return self.__horaMaxReserva

    def setCapacidad(self,nuevaCap):
        self.__capacidad = nuevaCap

    def setHoraMinReserva(self,nuevaHoraMin):
        self.__horaMinReserva = nuevaHoraMin

    def setHoraMaxReserva(self,nuevaHoraMax):
        self.__horaMaxReserva = nuevaHoraMax

    # Algoritmo de Marzullo
    def verificarDisponibilidad(self, horaIni, horaFin):
        reservas = []
        reservaIni = []
        reservaFin = []
        i = 0
    
        # Ciclo que escoge los intervalos a considerar en el algoritmo de Marzullo y los
        # ordena. No toma en cuenta aquellos que estan en la frontera del intervalo de la nueva
        # reservacion que se quiere agregar.
        while i < len(self.reservaciones):
            if (self.reservaciones[i][0] <= horaIni < self.reservaciones[i][1]) or (self.reservaciones[i][0] < horaFin <= self.reservaciones[i][1]):
                reservaIni.append([self.reservaciones[i][0],-1])
                reservaFin.append([self.reservaciones[i][1],1])
            i+=1
        reservaIni.sort()
        reservaFin.sort()
        reservas = reservaIni + reservaFin

        if reservas == []:
            self.reservaciones.append([horaIni,horaFin])
            return True
        
        cont = 0;
        mejor = 0;
        mejorInicio = reservas[0]
        mejorFin = reservas[1]
        pos = 2;    

        while cont >= mejor:
            if mejorInicio[1] == -1:
                cont += 1
                mejor += 1
                if mejorFin[1] == -1:
                    mejorInicio = mejorFin
                    mejorFin = reservas[pos]
                    pos += 1
                else:
                    cont -= 1

        if mejor >= self.__capacidad:            
            if (mejorInicio[0] > mejorFin[0]):
                aux = mejorInicio
                mejorInicio = mejorFin
                mejorFin = aux
            if ((horaFin != mejorInicio[0]) and (horaIni != mejorFin[0])):
                return False
        
        self.reservaciones.append([horaIni,horaFin])
        return True            
    
if __name__ == '__main__':
    est = Estacionamiento(10)
    formato = '%H:%M'
    
    while True:    
        while True:
            horaIni = raw_input("Introduzca hora del inicio de la reservacion (hh:mm): ")
            horaIni = datetime.strptime(str(horaIni), formato)
            if ((horaIni.minute == 0) and (est.getHoraMinReserva() <= horaIni.hour < est.getHoraMaxReserva())):
                break;
            else:
                print("Hora invalida.")

        while True:
            horaFin = raw_input("Introduzca hora de la finalizacion de la reservacion (hh:mm): ")
            horaFin = datetime.strptime(str(horaFin), formato)
            if ((horaFin.minute == 0) and (est.getHoraMinReserva() < horaFin.hour <= est.getHoraMaxReserva()) and (horaFin.hour > horaIni.hour)):
                break;
            else:
                print("Hora invalida.")
                
        if len(est.reservaciones) == 0:
            est.reservaciones.append([horaIni.hour,horaFin.hour])
            print("Se realizo una reservacion exitosa")
        else:
            if (est.verificarDisponibilidad(horaIni.hour, horaFin.hour)):
                print("Se realizo una reservacion exitosa")
            else:
                print("No se puede realizar la reserva solicitada")

        while True:
            continuar = raw_input("Desea hacer otra reservacion? (si/no): ")
            if (continuar != "si") and (continuar != "no"):
                print("Valor invalido.")
            else:
                break

        if continuar == "no":
            break