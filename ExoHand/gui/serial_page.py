from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout
from PyQt6.QtCore import Qt


class SerialPage(QWidget):

    def __init__(self):

        super().__init__()

        layout = QVBoxLayout()

        self.setLayout(layout)

        titulo = QLabel("Página de Puerto Serie")

        titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)

        titulo.setStyleSheet("""
            font-size:28px;
            font-weight:bold;
        """)

        layout.addWidget(titulo)