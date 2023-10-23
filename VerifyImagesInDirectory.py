import os
from os import listdir
from PIL import Image

def VerifyImagesInDirectory():
    app = Metashape.app
    inputDirectory = app.getExistingDirectory("Select the directory containing your images...")
    jpgGlobPattern = "*.[jJ][pP][gG]"
    imagePaths = list(Path(inputDirectory).rglob(jpgGlobPattern))

    count = 0
    for filename in imagePaths:
        try:
            im = Image.open(filename)
            im.verify()
            im.close()
            im = Image.open(filename) 
            im.transpose(Image.FLIP_LEFT_RIGHT)
            im.close()
        except(IOError,SyntaxError)as e:
            print(f'Found corrupt image: {filename}')
            count = count + 1

    # Show results
    app.messageBox(f'Found {count} bad files.')