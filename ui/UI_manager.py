import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication

#Clase Principal
class main_window(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("ui/main.ui", self)
        self.CommandSpeech.setText("")