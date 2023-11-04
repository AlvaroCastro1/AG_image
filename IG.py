import sys
import os
from PyQt6.QtWidgets import QApplication, QMainWindow,QFileDialog, QPushButton, QLabel, QSpinBox
from PyQt6.QtCore import Qt, QThread
from PyQt6.QtGui import QPixmap
import numpy as np
from PIL import Image
from solucion import Solucion
import random

class GUIApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setWindowTitle('Algoritmo Genético')
        self.setGeometry(100, 100, 800, 600)

        self.imagen_inicial = QLabel(self)
        self.imagen_inicial.setGeometry(10, 10, 300, 300)

        self.imagen_final = QLabel(self)
        self.imagen_final.setGeometry(450, 10, 300, 300)

        self.image_path = ""
        self.population_size = 100
        self.num_generations = 100

        self.image_button = QPushButton('Seleccionar Imagen', self)
        self.image_button.clicked.connect(self.load_image)
        self.image_button.setGeometry(50, 400, 200, 40)

        # Etiquetas para SpinBox
        self.population_label = QLabel('Población Inicial:', self)
        self.population_label.setGeometry(260, 370, 200, 40)

        self.population_spinbox = QSpinBox(self)
        self.population_spinbox.setGeometry(260, 400, 100, 40)
        self.population_spinbox.setValue(10)
        self.population_spinbox.setRange(1, 100)  # mínimo y máximo

        self.generations_label = QLabel('# de Generaciones:', self)
        self.generations_label.setGeometry(370, 370, 200, 40)

        self.generations_spinbox = QSpinBox(self)
        self.generations_spinbox.setGeometry(370, 400, 100, 40)
        self.generations_spinbox.setValue(10)
        self.generations_spinbox.setRange(1, 100)

        self.start_button = QPushButton('Iniciar Algoritmo', self)
        self.start_button.clicked.connect(self.start_algorithm)
        self.start_button.setGeometry(480, 400, 200, 40)

        self.informacion = QLabel("", self)
        self.informacion.setGeometry(450, 305, 300, 40)

    def load_image(self):
        fileFilter = 'Image File (*.jpg);'
        response = QFileDialog.getOpenFileName(
            parent=self,
            caption="Selecciona la imagen",
            directory=os.getcwd(),
            filter=fileFilter,
            initialFilter=fileFilter
        )

        if response:
            self.image_path = response[0]
            print("Ruta de la imagen seleccionada:", self.image_path)
            imagen_inicial = QPixmap(self.image_path)
            self.imagen_inicial.setPixmap(imagen_inicial.scaled(
                self.imagen_inicial.size(), Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation
            ))
            self.imagen_inicial.setScaledContents(True)

    def start_algorithm(self):
        if not self.image_path:
            print("Imagen no seleccionada")
        else:
            imagen_original = self.image_path
            poblacion_inicial = self.population_spinbox.value()
            num_generaciones = self.generations_spinbox.value()

            self.worker_thread = Trabajo_AG(self, imagen_original, poblacion_inicial, num_generaciones, self.imagen_final, self.informacion)
            self.worker_thread.finished.connect(self.worker_finished)
            self.worker_thread.start()

    def worker_finished(self):
        self.start_button.setEnabled(True)

class Trabajo_AG(QThread):
    def __init__(self, parent,imagen_original, poblacion_inicial, num_generaciones, cuadro_viewer, informacion):
        super().__init__()
        self.parent = parent
        self.imagen_original = Image.open(imagen_original)
        self.tamanio = self.imagen_original.size
        self.imgArray = np.array(self.imagen_original)
        self.num_soluciones = 0
        self.poblacion = []
        self.contador = 1
        self.ultima_aptitud = 0
        self.poblacion_inicial=poblacion_inicial
        self.num_generaciones=num_generaciones
        self.cuadro_viewer = cuadro_viewer
        self.informacion= informacion



    def run(self):
        self.crear_poblacion(self.poblacion_inicial)
        self.main(self.num_generaciones)
        self.finished.emit()

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
        ruta = ""
        if (x + 1 == num_generaciones):
            ruta = os.path.join("AG_trabajo", "respuesta_final.png")
            padre.getImagen().save(ruta)
            # exit(0)
        elif (x % 1 == 0):
            ruta = os.path.join("AG_trabajo", "generaciones", f"generacion{str(x)}.png")
            padre.getImagen().save(ruta)


        imagen_inicial = QPixmap(ruta)
        self.cuadro_viewer.setPixmap(imagen_inicial.scaled(
            self.cuadro_viewer.size(), Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation
        ))
        self.cuadro_viewer.setScaledContents(True)
        # print(ruta)

    def equilibrar(self, aptitud):
        cad = f"Aptitud: {aptitud}\t"
        print(cad)
        
        texto_actual = self.informacion.text()
        nuevo_contenido = texto_actual + cad
        self.informacion.setText(nuevo_contenido)
        
        
        if self.ultima_aptitud == aptitud:
            self.contador += 1
        else:
            self.ultima_aptitud = aptitud
            self.contador -= 1
            if self.contador < 1:
                self.contador = 1
        # print("Contador:", self.contador)

    def main(self, num_generaciones):
        print("Iniciando Generación")
        for x in range(num_generaciones):
            cad = f"Generación: {x + 1}/{num_generaciones}\t"
            print(cad)
            self.informacion.setText(cad)
            poblacion_ordenada = self.calcular_aptitud()
            self.equilibrar(poblacion_ordenada[0].getAptitud())
            self.guardar(poblacion_ordenada[0], x, num_generaciones)
            self.poblacion = poblacion_ordenada[:self.num_soluciones]
            self.cruzar(poblacion_ordenada[0])
            self.mutar()

def main():
    app = QApplication(sys.argv)
    window = GUIApp()
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
