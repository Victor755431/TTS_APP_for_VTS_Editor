# TTS_APP_for_VTS_Editor
This application was developped by Victor de CREVOISER
_____________________________________________________________________
        Instructions :
Execute Enregistreur.exe
Fill the form on the first page with :
    _ The path to a file extracted from VTS
    _ The path to the output folder
Then press the confirm button. The programm might take a few seconds to process the file.
The register interface should appear. 

        Description of the scrollArea :
On the right side of the page, you should see a scroll zone appear. 
It contains a graphical view of the replicas to register.
The replica colored in green is the selected replica.
The replicas in grey are the ones with an existing soundfile in the output folder.
The replicas in red are the ones without soundfiles in the output folder.

        Description of the buttons :
    The "•" button is the register button. Click once to start when you talk. The button becomes red.
Press it again, it goes back to its initial color, and the register sound gets transfered in the ouput folder.
    The "▶" button is the play button. It should be active only if a soundfile exists for the
selected replica. It plays that soundfile.
    The "⌫" button delete the associated soundfile.
    The ">>"button selects the next replica in the scrollArea.


_____________________________________________________________________
It was developped to register voices for a serious game produced by the LII team in ENAC.

If you want to use it in a personnal project, you might want to change the pictures in data/img/,
the characyer list in recorder.py, and repackage the app with pyinstaller.
_____________________________________________________________________
You are free to use it for whatever reason. If you need to edit it, please fork the project though.

For all questions, and possible bug report, please contact the developper at  :
                vdecrevoisier@gmail.com
_____________________________________________________________________

    Requirements : 
Please run 

    "pip install pyaudio wave PyQt5 pydub" 

before using the app.
_____________________________________________________________________
This is licensed GPL v3 because it contains a bundled app named Enregistreur.exe which includes PyQt5, which is protected by a GPL v3 license.

