from pathlib import Path

def GetFileNameWithExtension(path):
    return GetFileNameWithoutExtension(path) + GetFileExtension(path)

def GetFileNameWithoutExtension(path):
    return Path(path).stem

def GetFileExtension(path):
    # Includes the dot (for example, returns ".jpg")
    return Path(path).suffix