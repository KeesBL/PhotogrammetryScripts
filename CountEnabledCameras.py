import os
import Metashape

# This script will display the number of enabled 
# and disabled images in a messagebox.
#
# (c) Kees Beemster Leverenz 2022

# Define Script
def CountEnabledCameras():
    app = Metashape.app
    chunk = Metashape.app.document.chunk

    # Count cameras
    cameras_enabled = [camera for camera in chunk.cameras if camera.enabled == True]
    cameras_disabled = [camera for camera in chunk.cameras if camera.enabled == False]

    # Create message
    message = str(len(cameras_enabled)) + "/" + str(len(chunk.cameras)) + " cameras are enabled"
    app.messageBox(message)