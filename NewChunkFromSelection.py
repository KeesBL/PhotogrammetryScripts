import os
import Metashape

# This script will create a new chunk from the cameras selected 
# in the current chunk. Selected cameras in the existing chunk 
# will not be affected. 
#
# (c) Kees Beemster Leverenz 2022

# Define Script
def NewChunkFromSelection():
    app = Metashape.app
    doc = app.document
    chunks = doc.chunks

    # Define list of selected cameras from all chunks
    selectedCameras = list()

    # Grab selected cameras from all chunks
    for chunk in chunks:
        for camera in chunk.cameras:

            # Skip if camera is selected
            if camera.selected is False: continue
        
            # Add all selected cameras
            cameraPath = os.path.normpath(camera.photo.path)
            selectedCameras.append(cameraPath)
            app.update()

    # Guard: Abort if there are no cameras selected
    if (len(selectedCameras) == 0):
        print("No cameras selected, new chunk will not be created.")
        return

    # Create new chunk, add cameras
    doc.chunk = doc.addChunk()
    doc.chunk.addPhotos(selectedCameras)
    selectedCamerasCount = len(selectedCameras)
    print(f"New chunk created from {selectedCamerasCount} cameras!")