import Metashape
import os
from pathlib import Path

# When used, this script will attempt to relocate images that don't have a valid path.
# It will use the Camera's original file name and search the selected folder for 
# another file with exactly the same name. If found, it will automatically relocate the image.
# If there are zero filename matches or more than one filename match, the image will be skipped.
#
# (c) Kees Beemster Leverenz 2022

def RelocatePhotosRecursive():

    # Get directory that contains photos
    app = Metashape.app
    chunk = app.document.chunk
    inputDirectoryPath = app.getExistingDirectory("Select folder that contains your photos. Recursive search is performed")

    # Get photos (rglob is recursive)
    jpgGlobPattern = "*.[jJ][pP][gG]"
    photos = list(Path(inputDirectoryPath).rglob(jpgGlobPattern))

    # Loop through photos in current chunk
    locatedCameraCount = 0
    for camera in chunk.cameras:
    
        # [Guard] If the camera path exists, the camera is located
        cameraPathExists = os.path.isfile(camera.photo.path)
        if cameraPathExists: 
            locatedCameraCount += 1
            continue            

        # Get current file name and search for matching file names
        currentPath = camera.photo.path
        fileName = Path(currentPath).stem
        newPathOptions = [photo for photo in photos if Path(photo).stem == fileName]

        # Change path if exactly one match was found
        newPathOptionsCount = len(newPathOptions)
        if (newPathOptionsCount == 1): 
            camera.photo.path = os.path.join(inputDirectoryPath, newPathOptions[0])
            locatedCameraCount += 1
            print(f"{fileName} was relocated!")

        # Warn user about multiple matches found
        if (newPathOptionsCount > 1):
            print(f"{fileName} could not be automatically relocated. More than one matching filename exists.")

        # Warn user about zero matches found
        if (newPathOptionsCount == 0):
            print(f"{fileName} could not be automatically relocated. No matching filename exists.")

        # Keep UI alive
        app.update()

    # Completion message
    totalCameraCount = len(chunk.cameras)
    print(f"The recursive relocate process is finished: {locatedCameraCount}/{totalCameraCount} cameras located.")
    
Metashape.app.addMenuItem("Custom/Relocate Photos in Folder (Recursive)", RelocatePhotosRecursive)
