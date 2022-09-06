from PyQt5.QtWidgets import QMainWindow, QFileDialog, QVBoxLayout, QWidget, QLabel, QHBoxLayout, QLineEdit, QPushButton
from PyQt5.QtWidgets import QScrollArea, QFrame
from PyQt5.QtCore import pyqtSlot, Qt
import io
import line as l
import utilsVTS as utVTS
from recorder import Recorder

class SoundRecorder(QMainWindow):
    """Page principale de l'application.
    Selectionne l'entrée et la sortie, puis met en place le layout final, avec une scroll area à droite"""
    layout = None
    fileName = None
    data = None
    rec = None
    outputPath = None

    def __init__ (self):
        """Méthode appelée automatiquement à la création de la page"""
        super().__init__()
        self.resize(1200, 600)
        self.setWindowTitle ("SoundRecorder for VTS Editor")
        window2 = QWidget ()
        self.layout = QVBoxLayout(window2)
        self.setCentralWidget (window2)
        self.setupFileSelection()
        self.rec = Recorder(self)

    def setupFileSelection(self):
        """Mise en page de la sélection entrée/sortie"""
        fileSelectionWidget = QWidget()
        layout1 = QVBoxLayout(fileSelectionWidget)
        
        labelTitre = QLabel("STEP 1 : SELECT INPUT AND OUTPUT")
        labelTitre.setMaximumHeight(300)
        layout1.addWidget (labelTitre)

        line1 = QHBoxLayout()
        layout1.addLayout (line1)

        lineEdit1 = QLineEdit()
        lineEdit1.setPlaceholderText("Select an input file")
        line1.addWidget(lineEdit1)

        buttonLine1 = QPushButton("Choose input")
        buttonLine1.clicked.connect(lambda _:self.onSelectButton1Clicked(lineEdit1) )
        line1.addWidget(buttonLine1)

        line2 = QHBoxLayout()
        layout1.addLayout(line2)

        lineEdit2 = QLineEdit()
        lineEdit2.setPlaceholderText("Select an output folder")
        line2.addWidget (lineEdit2)

        buttonLine2 = QPushButton ("Choose output")
        buttonLine2.clicked.connect(lambda _:self.onSelectButton2Clicked(lineEdit2))
        line2.addWidget (buttonLine2)


        
        confirmButton = QPushButton("CONFIRM")
        confirmButton.clicked.connect(self.onConfirmButtonClicked)
        layout1.addWidget(confirmButton)

        self.layout.addWidget (fileSelectionWidget)
    
    def extractFromFile (self):
        with io.open(self.fileName,mode = "r",encoding="utf-8") as file:
            return utVTS.recolLignes(file.readlines()[2:])

    def toRecording(self):
        window2 = QWidget()
        self.setCentralWidget(window2)
        newLayout = QHBoxLayout(window2)
        self.layout = newLayout

        self.rec.setLigne(self.data[0])
        newLayout.addWidget(self.rec)

        scrollArea = QScrollArea ()
        scrollArea.setWidgetResizable(True)
        scrollArea.setFrameShape(QFrame.NoFrame)
        scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        scrollableArea = QWidget()
        scrollArea.setWidget(scrollableArea)
        scrollAreaLayout = QVBoxLayout()
        scrollAreaLayout.setContentsMargins(0, 0, 0, 0)
        scrollAreaLayout.setSpacing(0)
        scrollableArea.setLayout(scrollAreaLayout)
        scrollArea.setFixedWidth (250)
        newLayout.addWidget(scrollArea)

        for line in self.data:
            line.setupGraphics(scrollAreaLayout)

    def setLigne(self,l):
        self.rec.setLigne(l)

    @pyqtSlot()
    def onSelectButton1Clicked (self, lE):
        selectFilePath, _ = QFileDialog.getOpenFileName(self, "Choisir un fichier à lire", "", "All Files (*)")
        self.fileName = str(selectFilePath)
        lE.setText (selectFilePath)

    @pyqtSlot()
    def onSelectButton2Clicked (self, lE):
        selectFolderPath = QFileDialog.getExistingDirectory(self,"Choisir un dossier de sortie","")
        self.outputPath = selectFolderPath
        lE.setText (selectFolderPath)
    
    @pyqtSlot()
    def onConfirmButtonClicked (self):
        tempData = self.extractFromFile()
        self.data = [l.Line(self).fromLine(replique) for replique in tempData if l.Line(self).fromLine(replique) !=None]
        self.toRecording()
