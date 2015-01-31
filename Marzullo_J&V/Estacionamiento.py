'''
27/01/2015
 
Jorge Marcano : 11-10566
Maria Victoria Jorge : 11-10566
 
'''
 
class Estacionamiento :
     
    # Constructor
    def __init__(self,puestos): 
        self.reservaciones = []
        self.puestos = puestos
    
    # Algoritmo de marzullo modificado para devolver
    # una lista con todos los horarios en donde el 
    # estacionamiento esta lleno.     
    def marzullo(self,tabla,horaIni,horaFin):
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
            elif (best == cnt) and (best == self.puestos) :
                if (listaOut.count([tabla[i][0],tabla[i+1][0]]) == 0) and (tabla[i][0] != tabla[i+1][0]) :
                        listaOut.append([tabla[i][0],tabla[i+1][0]])
        
        listaOut.append([beststart,bestend])
        listaOut.append([best,0])
        return listaOut
    
    # Funcion que buscamos probar, 
    # devuelve True si la reservacion es valida
    # False en caso contrario. -1 en caso de error.
    def reservar(self,horaIni,horaFin) :
        
        # Verificacion de entrada
        if ((horaIni < 6) or (horaFin > 18)) or (horaFin-horaIni <= 0) :
            return -1
        
        reservaOrdenada = self.reservaciones
        reservaOrdenada.sort()
        reservaOrdenada.sort(key=lambda k: (k[0],-k[1]))
         
        listaIntervalo = self.marzullo(reservaOrdenada,horaIni,horaFin) # Devuelve la lista de todos los intervalos maximos
        best = listaIntervalo[len(listaIntervalo)-1][0] # Aqui esta el best 
        
        if (best == self.puestos):
            i = 0
            while (i<len(listaIntervalo)-1):
                if (((listaIntervalo[i][0] <= horaIni < listaIntervalo[i][1]) or (listaIntervalo[i][0] <  horaFin <= listaIntervalo[i][1])) or ((horaIni < listaIntervalo[i][0]) and (horaFin > listaIntervalo[i][1]))):
                    return False
                i = i + 1
        self.reservaciones.append([horaIni,-1]) # Se agregan las horas aceptadas a la lista de las reservas
        self.reservaciones.append([horaFin,1])
        return True
             