from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget


class ClickDetectionWidget(QWidget):
    """Classe qui permet à des widgets de se comprter comme des boutons. 
    Utilisée pour la classe line dans ce projet."""
    pressPos = None
    clicked = pyqtSignal()

    def mousePressEvent(self, event):
        self.pressPos = event.pos()

    def mouseReleaseEvent(self, event):
        # ensure that the left button was pressed *and* released within the
        # geometry of the widget; if so, emit the signal;
        if (self.pressPos is not None and 
            event.pos() in self.rect()):
                self.clicked.emit()
        self.pressPos = None