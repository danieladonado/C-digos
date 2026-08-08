from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout
from PyQt6.QtCore import Qt


class HomePage(QWidget):

    def __init__(self):

        super().__init__()

        layout = QVBoxLayout()

        self.setLayout(layout)

        layout.addStretch()

        titulo = QLabel("Bienvenido a EXOHAND")

        titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)

        titulo.setStyleSheet("""
            font-size:32px;
            font-weight:bold;
        """)

        layout.addWidget(titulo)

        descripcion = QLabel(
            "Sistema de rehabilitación mediante\n"
            "exoesqueleto"
        )

        descripcion.setAlignment(Qt.AlignmentFlag.AlignCenter)

        descripcion.setStyleSheet("""
            font-size:18px;
            color:gray;
        """)

        layout.addWidget(descripcion)

        icono = QLabel("🦾")

        icono.setAlignment(Qt.AlignmentFlag.AlignCenter)

        icono.setStyleSheet("""
            font-size:100px;
        """)

        layout.addWidget(icono)

        layout.addStretch()