from PyQt5.QtWidgets import QPushButton, QWidget, QLabel, QVBoxLayout, QHBoxLayout
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QPixmap, QFont

import os

import pyaudio
import wave
import threading
from pydub import AudioSegment
from pydub.playback import play

#         Liste des personnages officiels du serious game
# (à changer si vous utlisez l'application pour un autre projet)
#note : les noms doivent correspondre aux noms des images de data/img/
LISTE_PERSO =["Agente", "Alice", "Bruno", "Édouard", "Émilie", "Gérard", "Hubert", "Isabelle",
        "John", "Marc", "Marjorie", "Mathieu", "Mathilde", "Nurumbé", "Odile"]


#         Style sheets des boutons selon l'état de l'enregistreur.
RECORD_OFF_STYLESHEET = ""
RECORD_ON_STYLESHEET = "background-color : red"

RECORDED_STYLESHEET = ""
NOT_RECORDED_STYLESHEET = "background-color : grey"


class Recorder(QWidget):
    """Classe du Widget central de l'écran d'enregistrement
    Pemet 'afficher la réplique et de contrôler le fichier son associé"""
    line =None
    SR = None
    persoIcon=None
    persoLabel = None
    textLabel = None
    listenButton = None
    deleteButton = None
    recordButton = None

    isRecordOn = False

    def __init__(self,SR):
        """Initialisation de l'enregistreur"""
        super().__init__()
        self.SR = SR
        vertLayout = QVBoxLayout(self)

        box1 = QWidget()
        box1.setStyleSheet("")
        vertLayout.addWidget(box1)
        horLayout1 = QHBoxLayout (box1)

        self.persoIcon = QLabel ()
        pMap = QPixmap()
        self.persoIcon.setPixmap(pMap)
        self.persoIcon.setMaximumWidth (250)
        horLayout1.addWidget(self.persoIcon)

        self.persoLabel = QLabel ()
        self.persoLabel.setMaximumWidth(140)
        horLayout1.addWidget(self.persoLabel)

        self.textLabel = QLabel ()
        self.textLabel.setWordWrap(True)
        self.textLabel.setFont(QFont("Times",20))
        horLayout1.addWidget(self.textLabel)

        box2 = QWidget()
        box2.setMaximumHeight(150)
        box2.setStyleSheet("")
        horLayout2 = QHBoxLayout(box2)
        vertLayout.addWidget(box2)

        self.recordButton = QPushButton("•")
        self.recordButton.setToolTip ("Record audio")
        self.recordButton.setStyleSheet(RECORD_OFF_STYLESHEET)
        self.recordButton.clicked.connect(self.onRecordButton)
        horLayout2.addWidget(self.recordButton)

        self.listenButton = QPushButton("▶")
        self.listenButton.setToolTip ("Play recorded audio")
        self.listenButton.setStyleSheet(NOT_RECORDED_STYLESHEET)
        horLayout2.addWidget(self.listenButton)

        self.deleteButton = QPushButton("⌫")
        self.deleteButton.setToolTip ("Delete audio")
        self.deleteButton.setStyleSheet(NOT_RECORDED_STYLESHEET)
        horLayout2.addWidget(self.deleteButton)

        nextButton = QPushButton(">>")
        nextButton.setToolTip("Go to the next line")
        nextButton.clicked.connect(self.onNextButton)
        horLayout2.addWidget(nextButton)

    def setLigne(self,l):
        """Sélectionne une réplique. Permet de changer l'affichage"""
        if self.line:#  Important de vérifier ça, au lancement, self.line = None et None n'a pas de méthode
            self.line.selected =False
            self.line.displayStatus ()
            if self.isRecordOn :#Si l'enregistrement était en cours sur la réplique sélectionnée, on l'arrête.
                self.isRecordOn = False
        self.line=l
        self.persoLabel.setText(l.perso)
        self.textLabel.setText(l.textToPronounce)
        self.changeImage()
        l.selected = True
        l.displayStatus ()
        if l.recorded :
            self.listenButton.setStyleSheet(RECORDED_STYLESHEET)
            try :
                self.listenButton.clicked.disconnect()
            except Exception:
                pass#Si le bouton était déconnecté, il ne se passe rien
            self.listenButton.clicked.connect(self.readLineAudio)
            
            try :
                self.deleteButton.clicked.disconnect()
            except Exception:
                pass#Si le bouton était déconnecté, il ne se passe rien
            self.deleteButton.clicked.connect(self.deleteAudio)
            
            self.setStyleSheet(RECORDED_STYLESHEET)
        else :
            self.listenButton.setStyleSheet(NOT_RECORDED_STYLESHEET)
            self.listenButton.clicked.connect(self.doNothing)

            self.deleteButton.clicked.connect(self.doNothing)
            self.setStyleSheet(NOT_RECORDED_STYLESHEET)

    @pyqtSlot ()
    def onRecordButton (self):
        """Callback Qt qui démarre un thread d'enregistrement sonore"""
        if self.line.recorded:
            self.line.recorded = False
            self.deleteAudio()
        if self.isRecordOn :
            self.recordButton.setStyleSheet (RECORD_OFF_STYLESHEET)
            self.isRecordOn = False
        else :
            self.recordButton.setStyleSheet (RECORD_ON_STYLESHEET)
            thread = threading.Thread(target=self.record)            
            self.isRecordOn = True
            thread.start()
            


    def record(self):
        """Fonction appelée dans un thread séparé
        Enregistre le son en laissant l'application tourner"""
        p = pyaudio.PyAudio()
        stream = p.open(format=pyaudio.paInt16, channels=1, rate=44100, input=True, frames_per_buffer=1024)
        frames = []
        while self.isRecordOn:
            frames.append(stream.read(1024))
        stream.stop_stream()
        stream.close()
        p.terminate()

        wf = wave.open(self.line.savename, 'wb')
        wf.setnchannels(1)
        wf.setsampwidth(p.get_sample_size(pyaudio.paInt16))
        wf.setframerate(44100)
        wf.writeframes(b''.join(frames))
        wf.close()
        self.line.recorded = True
        self.line.displayStatus
        self.setLigne(self.line)


    @pyqtSlot()
    def onNextButton (self):
        """Callback Qt qui fait passer à la réplique suivante"""
        l = len(self.SR.data)
        if l >1 and self.line in self.SR.data:
            i = self.SR.data.index(self.line)
            if i < l-1:
                self.setLigne(self.SR.data[i+1])
                return None
            print("Already on last element")
            return None
        print("Erreur, redémarrez SVP...")
            

    @pyqtSlot()
    def doNothing (self):
        """Callback Qt qui ne fait rien"""
        pass

    @pyqtSlot()
    def readLineAudio (self):
        """Callback Qt qui ouvre le fichier enregistré, et le joue.
        Permet de vérifier l'audio."""
        print("Reading audio from {}".format(self.line.savename))
        if self.line.recorded :
            s = AudioSegment.from_wav (self.line.savename)
            play (s)

    @pyqtSlot()
    def deleteAudio (self):
        """Callback Qt qui supprime le fichier son associé à la ligne selectionnée"""
        self.line.recorded = False
        self.line.displayStatus()
        self.setLigne(self.line)
        try :
            os.remove(self.line.savename)
            print ("Audio deleted")
        except FileNotFoundError: #Si le fichier n'existait pas ou a été supprimé par l'utilisateur au runtime
            print ("404 : File not found")


    def changeImage(self):
        """Méthode qui change la photo du personnage"""
        if self.line.perso in ["APPRENANT"]:
            p = QPixmap()
            p.load(os.path.join("data","img","APPRENANT.jpg"))
            p.scaledToWidth(250)
            self.persoIcon.setPixmap(p)
        elif self.line.perso in LISTE_PERSO :
            p = QPixmap()
            p.load (os.path.join("data","img","{}.png".format(self.line.perso)))
            p.scaledToWidth(250)
            self.persoIcon.setPixmap(p)
        else :
            print ("Personnage inconnu au bataillon : [{}]".format(self.line.perso))
