from PyQt5.QtWidgets import QApplication
import sys
import soundRecorder as Sr

#Fichier de lancement de l'application.

if __name__ == "__main__":
    print("SoundRecorder Version 1.0\nBy Victor de CREVOISIER")
    app = QApplication(sys.argv)
    window = Sr.SoundRecorder()
    window.show()
    sys.exit(app.exec())