from asyncio import wait
import os
import sys

from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QFileDialog, QLabel, QSpinBox
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt


from AG import Generacion


class AGApp(QMainWindow):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Algoritmo Genético')
        self.setGeometry(100, 100, 800, 600)

        self.imagen_inicial = QLabel(self)
        self.imagen_inicial.setGeometry(10,10,300,300)

        self.imagen_final = QLabel(self)
        self.imagen_final.setGeometry(450,10,300,300)

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

    def set_population_size(self, value):
        self.population_size = value

    def set_num_generations(self, value):
        self.num_generations = value

    def start_algorithm(self):
        if not self.image_path:
            print("image null")
        else:
            imagen = self.image_path
            poblacion_inicial = self.population_spinbox.value()
            num_generaciones = self.generations_spinbox.value()
            
            gen = Generacion(imagen)
            gen.crear_poblacion(poblacion_inicial)
            gen.main(num_generaciones)


def main():
    app = QApplication(sys.argv)
    window = AGApp()
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
