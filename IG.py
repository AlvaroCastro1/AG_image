import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QFileDialog, QLabel, QSpinBox

from PIL import Image
import numpy as np
import os


class AGApp(QMainWindow):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Algoritmo Genético')
        self.setGeometry(100, 100, 800, 600)

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
        fileFilter = 'Image File (*.png *.jpg *.jpeg);'
        response = QFileDialog.getOpenFileName(
            parent=self,
            caption="Selecciona la imagen",
            directory=os.getcwd(),
            filter=fileFilter,
            initialFilter="Image File (*.png *.jpg *.jpeg)"
        )

        if response:
            self.image_path = response[0]
            print("Ruta de la imagen seleccionada:", self.image_path)

    def set_population_size(self, value):
        self.population_size = value

    def set_num_generations(self, value):
        self.num_generations = value


    def start_algorithm(self):

        if not self.image_path:
            print("image null")
        else:
            # print(self.image_path)
            # print(f"Poblacion Inicial: {self.population_spinbox.value()}")
            # print(f"Generaciones: {self.generations_spinbox.value()}")
            from AG import Generacion
            gen = Generacion(self.image_path)
            gen.crear_poblacion(self.population_spinbox.value())
            gen.main(self.generations_spinbox.value())



def main():
    app = QApplication(sys.argv)
    window = AGApp()
    window.show()
    sys.exit(app.exec())



if __name__ == '__main__':
    main()
