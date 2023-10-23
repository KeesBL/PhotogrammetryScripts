import Metashape
import os
import FileMethods
import ExifMethods
from PySide2 import QtWidgets, QtCore
from functools import partial
from pathlib import Path
from datetime import datetime
from PIL import Image

# This script renames images in the active chunk.
# The images are renamed in the OS, repathed, then relabeled
# Note this will not break the active chunk, but it may break
# other chunks. Use with caution.
#
# (c) Kees Beemster Leverenz 2022

def RenamePhotosInPlace():

    if CamerasAreLocated():
        # Define app
        app = QtWidgets.QApplication.instance()
        parent = app.activeWindow()

        # Warn user
        message = "WARNING: THE EFFECTS OF SCRIPT CANNOT BE UNDONE BY QUITTING WITHOUT SAVING. \n\n"
        message += "This script will rename image files in the OS, then repath and relabel photos in Metashape. "
        message += "This will not break the active chunk. However, it may break other chunks in the current project if they "
        message += "share references with photos in the current project. Use caution, and consider making a complete copy "
        message += "of your project and data before running this script. "
        Metashape.app.messageBox(message)

        # Open dialog
        dialog = RenameDialog(parent)
    else:
        Metashape.app.messageBox("One or more cameras are not located. Locate all cameras and try again.")

def CamerasAreLocated():
    chunk = Metashape.app.document.chunk
    for i in range(len(chunk.cameras)):
        cameraPathExists = os.path.isfile(chunk.cameras[i].photo.path)
        if cameraPathExists == False: return False;
    return True;

class RenameDialog(QtWidgets.QDialog):
    
    def __init__(self, parent):
        
        QtWidgets.QDialog.__init__(self, parent)
        self.setWindowTitle("Rename cameras in place")

        self.gridX = 2
        self.gridY = 2
        
        # Add input project name label
        projectNameLabel = QtWidgets.QLabel(self)
        projectNameLabel.setText("Project name:")

        # Add project name input
        projectNameInput = QtWidgets.QLineEdit(self)

        # Add rename button
        renameButton = QtWidgets.QPushButton("Rename Cameras", self)
        renameButton.clicked.connect(partial(RenameCameras, self, projectNameInput))

        # Add cancel button
        cancelButton = QtWidgets.QPushButton("Cancel", self)
        cancelButton.clicked.connect(partial(Cancel, self))

        # Create layout
        layout = QtWidgets.QGridLayout()
        layout.addWidget(projectNameLabel, 0, 0, QtCore.Qt.AlignRight)
        layout.addWidget(projectNameInput, 0, 1)
        layout.addWidget(renameButton, 1, 0)
        layout.addWidget(cancelButton, 1, 1)
        self.setLayout(layout)

        # Show
        self.show()
        self.adjustSize()
    
def RenameCameras(dialog, projectNameInput):

    # Set up
    projectName = projectNameInput.text()
    app = Metashape.app
    chunk = app.document.chunk

    # Check input is valid
    if projectName.strip() == "":
        app.messageBox("Project name cannot be blank.")

    # Rename
    # Output sample: {ProjectName} - {DateTaken} - Image {number}.jpg
    else:

        # Loop through cameras
        cameraCount = len(chunk.cameras)
        for i in range(cameraCount):

            # Get current path
            oldPath = chunk.cameras[i].photo.path
            oldFileNameWithExtension = FileMethods.GetFileNameWithExtension(oldPath)

            # Generate the new file name
            newFileNameWithExtension = GetNewFileNameWithExtension(projectName, oldPath, i)

            # Generate full new path
            newPath = oldPath \
            .replace(oldFileNameWithExtension, newFileNameWithExtension)

            # Rename file
            os.rename(oldPath, newPath)
            
            # Change camera photo path
            chunk.cameras[i].photo.path = newPath

            # Change camera label
            chunk.cameras[i].label = Path(newPath).stem

            # Keep UI alive
            app.update()
            
        app.messageBox("Rename complete!")
        dialog.reject()

def Cancel(dialog):
    dialog.reject()

def GetNewFileNameWithExtension(projectName, path, index):

    # Get base new file name
    newFileName = projectName

    # Add date taken, if available
    dateTaken = ExifMethods.GetExifDateTaken(path)
    if dateTaken != "" and dateTaken != None: 
        dateTakenString = dateTaken.strftime("%Y-%m-%dT%H-%M-%S")
        newFileName += f", {dateTakenString}"

    # Add author, if available
    photographer = ExifMethods.GetExifArtist(path)
    if photographer != "":
        newFileName += f", {photographer}"
        
    # Add index
    newFileName += f", Image_{index}"

    # Return 
    return newFileName + FileMethods.GetFileExtension(path)