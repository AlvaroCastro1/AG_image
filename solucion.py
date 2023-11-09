import random
from PIL import Image, ImageDraw
import numpy as np
import colour
#color random
def getColorRandom(): 
    # generar color aleatorio RGB
    return (random.randint(0,255), random.randint(0, 255), random.randint(0, 255) )

class Solucion():

    def __init__(self, tamanio:tuple[int, int], tipo:str, imagen:Image=None) -> None:
        self.tamanio = tamanio
        self.tipo = tipo
        self.imagen = imagen if imagen is not None else Image.new('RGB', tamanio, getColorRandom()) #valida si la imagen es nula
        #self.imagen = imagen if imagen != None else Image.new(type, tamanio, getColorRandom())
        # Imagen para dibujar
        self.draw = ImageDraw.Draw(self.imagen) #lienzo para pintar 
        self.imgArray = [] if imagen == None else np.array(self.imagen) #matriz imagen
        self.aptitud = -1 #se inicializa

    def getImagen(self):
        return self.imagen

    def pintarFigura(self, num_figuras:int=-1, subdivision:int=8) -> None:
        if num_figuras == -1:
            num_figuras = random.randint(3, 6)
        #la region donde se generan los puntos aleatorios para los vértices delos poligonos
        region = (int(self.tamanio[0] / subdivision), int(self.tamanio[1] / subdivision))
        for _ in range(num_figuras):
            num_puntos_poligono = random.randint(3, 6)
            pos = (random.randint(0, self.tamanio[0]), random.randint(0, self.tamanio[1]))
            #coordenadas de los vertices del poligono
            puntos = []
            for _ in range(num_puntos_poligono):
                puntos.append((random.randint(pos[0] - region[0], pos[0] + region[0]),
                           random.randint(pos[1] - region[1], pos[1] + region[1])))
            #dibujar poligono usando vertices
            self.draw.polygon(puntos, fill=getColorRandom())
            # actualizar imgArray, convirtiendo la imagen en una matriz NumPy
            self.imgArray = np.array(self.imagen)

    # imagen objetivo con la que se comparara
    def getAptitud(self, targetImage=None) -> float:
        # no se ha calculado antes
        if (self.aptitud == -1):
            # media de la diferencia de color entre la imagen del objeto y la imagen objetivo 
            # delta_E de colour calcula la diferencia de color entre las dos imagenes
            self.aptitud = np.mean(colour.delta_E(self.imgArray, targetImage, method='CIE1976'))
        return self.aptitud
    def __str__(self):
        return f"Solucion con aptitud: ({self.aptitud})"
# entre mas cercano a 0 mas mejor