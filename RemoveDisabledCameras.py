import Metashape
from PySide2 import QtWidgets, QtCore
from functools import partial

# This script will prompt the user, then remove disabled
# cameras if requested.
#
# (c) Kees Beemster Leverenz 2022

def PromptUserToRemove():

    # Define app
    app = QtWidgets.QApplication.instance()
    parent = app.activeWindow()

    # Open dialog
    dialog = RemoveDialog(parent)

class RemoveDialog(QtWidgets.QDialog):

     def __init__(self, parent):
        
            QtWidgets.QDialog.__init__(self, parent)
            chunk = Metashape.app.document.chunk
            disabledCameras = [camera for camera in chunk.cameras if camera.enabled == False]
            disabledCamerasCount = len(disabledCameras)
            self.setWindowTitle(f"Remove {disabledCamerasCount} disabled cameras?")
            self.gridX = 2
            self.gridY = 1

            # Add remove button
            removeButton = QtWidgets.QPushButton("Remove Disabled Cameras", self)
            removeButton.clicked.connect(partial(RemoveDisabledCameras, self, disabledCameras))

            # Add cancel button
            cancelButton = QtWidgets.QPushButton("Cancel", self)
            cancelButton.clicked.connect(partial(Cancel, self))

            # Create layout
            layout = QtWidgets.QGridLayout()
            layout.addWidget(removeButton, 0, 0)
            layout.addWidget(cancelButton, 0, 1)
            self.setLayout(layout)

            # Show
            self.show()
            self.adjustSize()
    
def RemoveDisabledCameras(dialog, disabledCameras):
    app = Metashape.app
    chunk = Metashape.app.document.chunk
    chunk.remove(disabledCameras)
    disabledCamerasCount = len(disabledCameras)
    app.messageBox(f"{disabledCamerasCount} disabled camera(s) removed.")
    dialog.reject()

def Cancel(dialog):
    dialog.reject()