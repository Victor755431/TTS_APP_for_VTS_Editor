import os
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel
from PyQt5.QtCore import pyqtSlot
from clickDetectionWidget import ClickDetectionWidget

TO_READ_STYLESHEET = "background-color : red"
READING_STYLESHEET = "background-color : lime "
ALREADY_READ_STYLESHEET = "background-color : lightgrey"
PATH_TO_TEMP_SOUND_FILES = "alreadyRecorded"

class Line(ClickDetectionWidget):
    """Classe représentant une réplique. 
    Stocke des informations relatives à la réplique. 
    Inclus une représentation graphique dans la scroll area du soundRecorder."""
    SR = None
    savename = None
    textToPronounce = None
    perso = None
    pathAudioTemp = None
    recorded = False
    selected = False

    def __init__(self, SR):
        """Méthode de création"""
        super().__init__()
        self.SR=SR
        self.savename =""
        self.textToPronounce = ""
        self.pathAudioTemp =""
    
    def fromLine (self, line) :
        """Prend une ligne du fichier VTS et extrait les données utiles pour l'enregistrement des voix"""
        liste = line.split('\t')
        if not self.SR.outputPath :
            self.savename = os.path.join(PATH_TO_TEMP_SOUND_FILES, liste[0])
        else :
            self.savename = os.path.join(PATH_TO_TEMP_SOUND_FILES, "{}.wav".format(liste[0]))
        self.textToPronounce = liste[1] if liste[1] != "" else liste[2]
        if self.textToPronounce == "":
            return None
        self.perso = liste[3]
        self.recorded = os.path.exists(self.savename)
        return (self)
    
    def __repr__(self):
        """Représentation en string"""
        return "{} : {} ({})\n".format(self.perso, self.textToPronounce, self.savename)

    def setupGraphics(self, layoutExt):
        """Métode qui crée l'affichage graphique de la ligne dans la scroll area"""
        layout = QHBoxLayout(self)
        self.displayStatus()
        layout.addWidget(QLabel(self.perso))
        layout.addWidget(QLabel(self.textToPronounce))
        layoutExt.addWidget(self)
        self.clicked.connect(self.onClicked)

    def displayStatus (self):
        """Méthode qui change la stylesheet de la ligne selon son état"""
        if(self.recorded):
            self.setStyleSheet(ALREADY_READ_STYLESHEET)
        else :
            self.setStyleSheet (TO_READ_STYLESHEET)

        if self.selected :
            self.setStyleSheet (READING_STYLESHEET)
    
    @pyqtSlot()
    def onClicked(self):
        """Callback de Qt.
        Fait qu'une ligne cliquée dans la scroll bar devient la ligne selectionée."""
        self.SR.setLigne(self)
