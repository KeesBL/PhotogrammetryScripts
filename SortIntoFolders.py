import os
import shutil
import Metashape
import FileMethods
import ExifMethods
from datetime import datetime,date
from PIL import Image
from pathlib import Path

# This script recursively grabs all images from a directory, 
# then sorts them into a series of folders in the that directroy.
# Each folder will contain images from a single day, named according 
# to the day that image was taken. Images without a date will be
# placed in separate folder. 
# 
# (c) Kees Beemster Leverenz 2022

# Get info from video
def SortIntoFolders():
    app = Metashape.app

    # Warn user
    message = "WARNING: THE EFFECTS OF SCRIPT CANNOT BE UNDONE BY QUITTING WITHOUT SAVING. \n\n"
    message += "This script will sort all images in the selected directory. The process cannot be undone. "
    message += "Be sure you have the correct folder selected when running this script!"
    app.messageBox(message)

    # Get input folder
    inputDirectory = app.getExistingDirectory("Select the directory containing your images...")
    inputDirectory = os.path.normpath(inputDirectory)

    # Confirm with user
    confirmValue = app.getString(f"Selected folder is: {inputDirectory}\nType ok to sort...")
    if (confirmValue != "ok"):
        print("Sort operation was not confirmed.")
        return
    print(f"Sorting {inputDirectory}...")

    # Get images in input folder (rglob is recursive)
    jpgGlobPattern = "*.[jJ][pP][gG]"
    imagePaths = list(Path(inputDirectory).rglob(jpgGlobPattern))
    print(f"{len(imagePaths)} images found...")

    # Sort
    for imagePath in imagePaths:
        # Don't freeze
        app.update()

        # Identify the name of the folder the image belongs in
        # (This is the date like "04-Dec-2022")
        directoryNameForPhoto = GetDirectoryNameFromPhotoPath(imagePath)

        # Determine the full path to the destination directory
        newDirectoryPath = os.path.join(inputDirectory, directoryNameForPhoto)

        # Check if the directory exists, and create it if needed
        pathExists = os.path.exists(newDirectoryPath)
        if not pathExists: 
            os.mkdir(newDirectoryPath)
            print(f"New folder created: {newDirectoryPath}!")

        # Determine full oldPath and newPath 
        oldPath = imagePath
        fileNameWithExtension = FileMethods.GetFileNameWithExtension(oldPath)
        newPath = os.path.join(newDirectoryPath, fileNameWithExtension)

        # [Guard] Skip this image if the file is already sorted
        if os.path.samefile(oldPath, newPath):
            print(f"{oldPath} is sorted: it does not need to be moved.")
            continue

        # [Guard] Check for file name overlaps
        fileNameOverlap = os.path.exists(newPath)
        if fileNameOverlap:
            print(f"{oldPath} can't be sorted: a file at the destination exists with the same name.")
            continue
            
        # Actually move -- shutil is NAS compatible
        shutil.move(oldPath, newPath)
        print(f"{fileNameWithExtension} has been sorted.")

    print("Image sorting complete!")

def GetDirectoryNameFromPhotoPath(path):
    directoryName = ""

    # Add date
    takenDate = ExifMethods.GetExifDateTaken(path)
    if (takenDate != ""): 
        directoryName += takenDate.strftime("%Y-%b-%d")
    else:
        directoryName += "No Date"

    # Add photographer, if available
    photographer = ExifMethods.GetExifArtist(path)
    if (photographer != ""): 
        directoryName += f", {photographer}"

    return directoryName
