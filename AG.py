from PIL import Image
import random
import numpy as np
import sys
import os
from solucion import Solucion

class Generacion:
    def __init__(self, imagen_original):
        self.imagen_original = Image.open(imagen_original)
        self.tamanio = self.imagen_original.size
        self.imgArray = np.array(self.imagen_original)
        self.num_soluciones = 0
        self.poblacion = []
        self.contador = 1
        self.ultima_aptitud = 0

    def crear_poblacion(self, num_soluciones, imagen_previa=None):
        self.num_soluciones = num_soluciones
        if imagen_previa is not None:
            for _ in range(num_soluciones - 1):
                img = Image.open(imagen_previa) 
                self.poblacion.append(Solucion(self.tamanio, self.imagen_original.mode, img))
            for x in self.poblacion:
                x.pintarFigura(1, subdivision=1)
            img = Image.open(imagen_previa)
            self.poblacion.append(Solucion(self.tamanio, self.imagen_original.mode, img))
        else:
            for _ in range(num_soluciones):
                self.poblacion.append(Solucion(self.tamanio, self.imagen_original.mode))
            for x in self.poblacion:
                x.pintarFigura()
        print(f"Población creada con {num_soluciones} soluciones.")

    def calcular_aptitud(self):
        return sorted(self.poblacion, key=lambda x: x.getAptitud(self.imgArray))

    def cruzar(self, padre):
        res = [padre]
        for s in self.poblacion:
            if s != padre:
                punto_corte = random.randint(0, self.tamanio[0])
                imagen_h1 = Image.new(self.imagen_original.mode, self.tamanio, (0, 0, 0))
                imagen_h1.paste(padre.getImagen().crop((0, 0, punto_corte, self.tamanio[1])), (0, 0))
                imagen_h1.paste(s.getImagen().crop((punto_corte, 0, self.tamanio[0], self.tamanio[1])), (punto_corte, 0))
                res.append(Solucion(self.tamanio, self.imagen_original.mode, imagen_h1))
                imagen_h2 = Image.new(self.imagen_original.mode, self.tamanio, (0, 0, 0))
                imagen_h2.paste(s.getImagen().crop((0, 0, punto_corte, self.tamanio[1])), (0, 0))
                imagen_h2.paste(padre.getImagen().crop((punto_corte, 0, self.tamanio[0], self.tamanio[1])), (punto_corte, 0))
                res.append(Solucion(self.tamanio, self.imagen_original.mode, imagen_h2))
        self.poblacion = res

    def mutar(self):
        is_padre = True
        for solucion in self.poblacion:
            if is_padre:
                is_padre = False
            else:
                solucion.pintarFigura(1, subdivision=self.contador)

    def guardar(self, padre: Solucion, x: int, num_generaciones: int) -> None:
        if not os.path.exists("AG_trabajo"):
            os.makedirs("AG_trabajo")
        if not os.path.exists("AG_trabajo/generaciones"):
            os.makedirs("AG_trabajo/generaciones")

        if (x + 1 == num_generaciones):
            ruta = os.path.join("AG_trabajo", "respuesta_final.png")
            padre.getImagen().save(ruta)
            exit(0)
        elif (x % 1 == 0):
            ruta = os.path.join("AG_trabajo", "generaciones", f"generacion{str(x)}.png")
            padre.getImagen().save(ruta)


    def equilibrar(self, aptitud):
        print("Aptitud: ", aptitud, end="\t")
        if self.ultima_aptitud == aptitud:
            self.contador += 1
        else:
            self.ultima_aptitud = aptitud
            self.contador -= 1
            if self.contador < 1:
                self.contador = 1
        print("Contador:", self.contador)

    def main(self, num_generaciones):
        print("Iniciando Generación")
        for x in range(num_generaciones):
            print(f"Generación: {x + 1}/{num_generaciones}", end="\t")
            poblacion_ordenada = self.calcular_aptitud()
            self.equilibrar(poblacion_ordenada[0].getAptitud())
            self.guardar(poblacion_ordenada[0], x, num_generaciones)
            self.poblacion = poblacion_ordenada[:self.num_soluciones]
            self.cruzar(poblacion_ordenada[0])
            self.mutar()

# Obtener datos desde la terminal
argumentos_terminal = sys.argv

if len(argumentos_terminal) == 4:
    gen = Generacion(argumentos_terminal[1])
    gen.crear_poblacion(int(argumentos_terminal[2]))
    gen.main(int(argumentos_terminal[3]))
elif len(argumentos_terminal) == 5:
    gen = Generacion(argumentos_terminal[1])
    gen.crear_poblacion(int(argumentos_terminal[2]), argumentos_terminal[4])
    gen.main(int(argumentos_terminal[3]))
else:
    print("Por favor usa: python AG.py [imagen] [numero de soluciones inicial] [numero de Generaciones]")
    print("\Ejemplo: python AG.py imagen1.png 100 500\n")
    print("En caso de querer cargar una generación anterior:")
    print("Usa: python AG.py [imagen]  [numero de soluciones inicial] [numero de Generaciones] [img previa]")
    print("\tEJEMPLO: python AG.py image.png 100 500 load.png")
