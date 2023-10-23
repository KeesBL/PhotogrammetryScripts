import os
import Metashape

# This script will disable every other camera 
# in the active chunk.
#
# (c) Kees Beemster Leverenz 2023

# Define Script
def DisableEveryOtherCamera():
    app = Metashape.app
    chunk = Metashape.app.document.chunk
    cameras = chunk.cameras
    count = 0

    # Loop through cameras and disable every other camera
    for camera in cameras:
        if (count % 2) == 0:
            camera.enabled = False
        count +=1

    # Note completion
    app.messageBox("Every other camera disabled.")