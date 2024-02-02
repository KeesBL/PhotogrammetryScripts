import Metashape
import os
from pathlib import Path

# Adds JPGs in a specified folder that are not 
# already added in the current chunk.
#
# Kees Beemster Leverenz 2024

def AddNewPhotosFromFolder():
    app = Metashape.app
    doc = app.document
    chunk = doc.chunk
    cameras = doc.chunk.cameras

    # Get new photo paths
    newPhotosDirectory = Metashape.app.getExistingDirectory("Specify input photo folder:")
    newPhotosPaths = list(Path(newPhotosDirectory).rglob("*.[jJ][pP][gG]"))

    # Get existing photo paths
    existingPhotosPaths = list()
    for camera in chunk.cameras:
        existingPhotosPaths.append(Path(camera.photo.path))

    # Create a list of all new photo paths except existing photo paths
    # Path() converts each item to a WindowsPath, which cannot be added directly.
    # This is why str(item) is required to convert them to a straight string, which
    # Metashape can add. 
    photoPathsToAdd = [str(item) for item in newPhotosPaths if item not in existingPhotosPaths]

    # Add those photos
    chunk.addPhotos(photoPathsToAdd)
    app.messageBox(str(len(photoPathsToAdd)) + " photo(s) added.")
