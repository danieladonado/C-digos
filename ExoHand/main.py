"""
EXOHAND
    main.py
    Punto de entrada de toda la aplicacion.

"""

import sys

from PyQt6.QtWidgets import QApplication

# Ventana principal
from gui.main_window import MainWindow


def main():
    """
    Inicia la aplicación.
    """

    app = QApplication(sys.argv)

    #Nombre de la aplicación
    app.setApplicationName("EXOHAND")

    #Crear ventana principal
    window = MainWindow()

    #Mostrar ventana
    window.show()

    #Ejecutar
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
    