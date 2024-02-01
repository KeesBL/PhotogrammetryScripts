import os
import Metashape

# This script will remove duplicate cameras in the active chunk.
# Unlike the Agisoft published script, this script will prioritize the 
# removal of cameras that are not aligned, when some aligned and some 
# unaligned duplicate cameras exist. 
#
# Kees Beemster Leverenz 2024

# Function to check camera alignment
def IsAligned(camera):
    if camera.transform and camera.type == Metashape.Camera.Type.Regular: return True
    return False

# Define main script
def DeduplicateCamerasPrioritizeUnaligned():
    app = Metashape.app
    chunk = Metashape.app.document.chunk
    camerasDictionary = dict()
    camerasToRemove = list()

    # Loop through cameras to identify which to remove
    for camera in chunk.cameras:

        # If the current camera is not in the dictionary, 
        # add the camera to the dictionary and continue.
        cameraPath = camera.photo.path
        dictionaryCamera = camerasDictionary.get(cameraPath)
        if dictionaryCamera == None:
            camerasDictionary[cameraPath] = camera
            continue

        # If the current camera is in the dictionary, we need to make 
        # some decisions:

	# 1) Remove the current camera, if it is not aligned.
        if not IsAligned(camera): 
            camerasToRemove.append(camera)
            continue

        # 2) Remove the current camera, if the dictionary camera is aligned.
        if IsAligned(dictionaryCamera): 
            camerasToRemove.append(camera)
            continue

        # 3) At this point, the current camera is aligned and the dictionary camera is not.
	# Replace the dictionary camera with the current camera.
        del camerasDictionary[cameraPath]
        camerasDictionary[cameraPath] = camera

    # Remove cameras. This updates the point cloud, so performance 
    # is better if it is done all at once.
    removalCount = len(camerasToRemove)
    chunk.remove(camerasToRemove)

    # Note completion
    app.messageBox(str(removalCount) + " duplicates removed.")