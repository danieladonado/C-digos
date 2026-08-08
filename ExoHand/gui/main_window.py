from PyQt6.QtWidgets import (
    QMainWindow,
    QWidget,
    QPushButton,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QFrame,
    QStatusBar,
    QStackedWidget
)

from PyQt6.QtCore import Qt


from gui.home_page import HomePage
from gui.camera_page import CameraPage
from gui.therapy_page import TherapyPage
from gui.calibration_page import CalibrationPage
from gui.serial_page import SerialPage
from gui.history_page import HistoryPage


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("EXOHAND")
        self.resize(1400, 850)

        self.create_ui()

    def create_ui(self):

        
        #WIDGET CENTRAL
    
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        central_widget.setLayout(main_layout)

        
        #MENÚ
    
        menu = QFrame()
        menu.setFixedWidth(230)

        menu.setStyleSheet("""
            QFrame{
                background-color:#1F2937;
            }
        """)

        menu_layout = QVBoxLayout()
        menu_layout.setContentsMargins(10,20,10,20)
        menu_layout.setSpacing(10)

        menu.setLayout(menu_layout)

    
        #TÍTULO
        titulo = QLabel("EXOHAND")

        titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)

        titulo.setStyleSheet("""
            color:white;
            font-size:24px;
            font-weight:bold;
            padding:15px;
        """)

        menu_layout.addWidget(titulo)

        
        #ESTILO
        estilo_boton = """
            QPushButton{

                background-color:#374151;

                color:white;

                border:none;

                border-radius:8px;

                padding:12px;

                text-align:left;

                font-size:15px;

            }

            QPushButton:hover{

                background-color:#4B5563;

            }

            QPushButton:pressed{

                background-color:#2563EB;

            }
        """


        #BOTONES
        self.btn_inicio = QPushButton("Inicio")
        self.btn_camara = QPushButton("Cámara")
        self.btn_serial = QPushButton("Exoesqueleto")
        self.btn_calibracion = QPushButton("Calibración")
        self.btn_terapia = QPushButton("Terapia")
        self.btn_historial = QPushButton("Historial")

        botones = [
            self.btn_inicio,
            self.btn_camara,
            self.btn_serial,
            self.btn_calibracion,
            self.btn_terapia,
            self.btn_historial
        ]

        for boton in botones:

            boton.setMinimumHeight(45)
            boton.setStyleSheet(estilo_boton)
            menu_layout.addWidget(boton)

        menu_layout.addStretch()

        
        #STACK DE PÁGINAS

        self.stack = QStackedWidget()

        self.home_page = HomePage()
        self.camera_page = CameraPage()
        self.serial_page = SerialPage()
        self.calibration_page = CalibrationPage()
        self.therapy_page = TherapyPage()
        self.history_page = HistoryPage()

        self.stack.addWidget(self.home_page)
        self.stack.addWidget(self.camera_page)
        self.stack.addWidget(self.serial_page)
        self.stack.addWidget(self.calibration_page)
        self.stack.addWidget(self.therapy_page)
        self.stack.addWidget(self.history_page)

        
        #CAMBIO DE PÁGINAS
        self.btn_inicio.clicked.connect(
            lambda: self.stack.setCurrentIndex(0)
        )

        self.btn_camara.clicked.connect(
            lambda: self.stack.setCurrentIndex(1)
        )

        self.btn_serial.clicked.connect(
            lambda: self.stack.setCurrentIndex(2)
        )

        self.btn_calibracion.clicked.connect(
            lambda: self.stack.setCurrentIndex(3)
        )

        self.btn_terapia.clicked.connect(
            lambda: self.stack.setCurrentIndex(4)
        )

        self.btn_historial.clicked.connect(
            lambda: self.stack.setCurrentIndex(5)
        )

    
        #AGREGAR AL LAYOUT PRINCIPAL
        main_layout.addWidget(menu)
        main_layout.addWidget(self.stack)

        
        #STATUS BARRA
        self.status = QStatusBar()

        self.status.showMessage("Sistema listo")

        self.setStatusBar(self.status)