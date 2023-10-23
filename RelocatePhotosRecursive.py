import Metashape
import os
from pathlib import Path

# When used, this script will attempt to relocate images that don't have a valid path.
# It will use the Camera's original file name and search the selected folder for 
# another file with exactly the same name. If found, it will automatically relocate the image.
# If there are zero filename matches or more than one filename match, the image will be skipped.
#
# (c) Kees Beemster Leverenz 2023

def RelocatePhotosRecursive():

    # Get directory that contains photos
    app = Metashape.app
    chunk = app.document.chunk
    inputDirectoryPath = app.getExistingDirectory("Select folder that contains your photos. Recursive search is performed")

    # Get photos (rglob is recursive)
    jpgGlobPattern = "*.[jJ][pP][gG]"
    pngGlobPattern = "*.[pP][nN][gG]"
    jpgFiles = list(Path(inputDirectoryPath).rglob(jpgGlobPattern))
    pngFiles = list(Path(inputDirectoryPath).rglob(pngGlobPattern))
    photos = jpgFiles + pngFiles

    # Create an index to look up photo paths by their filename
    # Only distinct filenames are used here. 
    # Any image with more than one path per file name is ignored.
    photoNames = [path.name for path in photos]
    photosIndex = {} 
    for photo in photos:
        if (photoNames.count(photo.name) == 1):
            photosIndex[photo.name] = photo

    # Loop through photos in current chunk
    locatedCameraCount = 0
    currentCamera = 0
    output = ""
    totalCameras = len(chunk.cameras)
    for camera in chunk.cameras:
    
        # Record progress
        currentCamera += 1

        # [Guard] If the camera path exists, the camera is already located and can be ignored
        cameraPathExists = os.path.isfile(camera.photo.path)
        if cameraPathExists: 
            locatedCameraCount += 1
            continue            

        # Get the current camera's file name
        fileName = Path(camera.photo.path).name

        # Check if a match is found
        if fileName in photosIndex:
            camera.photo.path = str(photosIndex[fileName])
            locatedCameraCount += 1
        else:
            output += f"The photo '{fileName}' does not have a match or unique match.\n"

        # Report progress
        if (currentCamera % 100 == 0):
            print(f"{currentCamera}/{totalCameras} cameras processed. {locatedCameraCount} cameras found.")

        # Keep UI alive
        app.update()

    # Completion message
    totalCameraCount = len(chunk.cameras)
    app.messageBox(f"The recursive relocate process is finished: {locatedCameraCount}/{totalCameraCount} cameras located.")
