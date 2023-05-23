import Metashape
import os
from pathlib import Path

# This script will add all JPG images in a folder
# including all subfolders of that folder. 
#
# (c) Kees Beemster Leverenz 2022

# Get folder path
app = Metashape.app
message = "Select folder that contains your photos. Photos must be in .jpg format. "
message += "Photos in all subfolders will also be added to the current chunk."
path = Metashape.app.getExistingDirectory(message)

# Get photos (rglob is recursive)
caseInsensitiveJpgPattern = "*.[jJ][pP][gG]"
photos = list(Path(path).rglob(caseInsensitiveJpgPattern))

# Generate list of full paths
photoPaths = list()
print("Loading photos...")
for photo in photos:
	photoPath = os.path.join(path,photo)
	photoPaths.append(photoPath)
	Metashape.app.update()
    
# Add photos
Metashape.app.document.chunk.addPhotos(photoPaths)