from PIL import Image
from datetime import datetime

# Tag meanings: https://exiv2.org/tags.html

def GetExifArtist(path):
    try:
        exif = Image.open(path).getexif()
        artistTag = 315
        artist = exif.get(artistTag)
        if (artist == None): return ""
        if (artist == ""): return ""
        return artist

    except:
        return ""

def GetExifDateTaken(path):
    
    # Returns the exif date taken from the camera, if available.
    try:
        exif = Image.open(path).getexif()
        creationDateTimeTag = 306
        dateTakenString = exif.get(creationDateTimeTag)
        return datetime.strptime(dateTakenString, "%Y:%m:%d %H:%M:%S")

    except:
       return ""