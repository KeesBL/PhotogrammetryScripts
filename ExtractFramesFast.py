import ffmpeg
import Metashape
import subprocess
import threading
import os
import glob
import subprocess
import FileMethods
from wand.image import Image
from pathlib import Path

# This script extracts still images from a video file.
# Performance is typically much better than realtime.
# 
# (c) Kees Beemster Leverenz 2022

# Get info from video
def ExtractFramesFast_Ffmpeg():

    app = Metashape.app

    # Get input video
    inputVideoPath = app.getOpenFileName("Select your input video file...", "", "*.mp4 *.mov *.avi *.flv *.mkv *.wmv")
    if (inputVideoPath == ""): return
    inputVideoName = os.path.normpath(inputVideoPath)
    inputVideoName = GetFileName(inputVideoPath)
    print(f"Input video: {inputVideoPath}")

    # Construct output format
    outputDirectory = app.getExistingDirectory("Select your output directory...", )
    if (outputDirectory == ""): return
    outputDirectory = os.path.normpath(outputDirectory)
    outputTemplate = os.path.join(outputDirectory, f"{inputVideoName}_Frame_%0000d.bmp")
    print(f"Output directory: {outputDirectory}")

    # Get frame rate
    desiredExtractionFrameRate = app \
    .getInt("Input frames to extract per second (for example, 1 = one frame every second)...", 1)
    if (desiredExtractionFrameRate == None): return

    # Extract frames
    os.startfile(outputDirectory)
    process = (ffmpeg \
    .input(inputVideoPath) \
    .filter_('fps', fps=desiredExtractionFrameRate) \
    .output(outputTemplate) \
    .run_async(pipe_stdin=True))
    process.wait()

    # Note progress
    print("Frame extraction complete! Converting to JPG...")

    # Convert to bmp
    bmpSearchPattern = os.path.join(outputDirectory, f"{inputVideoName}_Frame_*.bmp")
    bmpImages = glob.glob(bmpSearchPattern)
    for bmpImage in bmpImages:
        ConvertToJpg(bmpImage)
        imageName = GetFileName(bmpImage)
        print(f"Converted {imageName} to JPG")
        app.update()

    # Note progress
    print("Process complete!")

def ConvertToJpg(oldImagePath):
    # While ffmpeg can convert to jpg, 
    # the quality is poor. Using ImageMagick
    # produces a much higher quality result.
    
    # Set up
    outputDirectory = os.path.dirname(oldImagePath)
    fileName = FileMethods.GetFileNameWithoutExtension(oldImagePath)

    # Convert
    with Image(filename=oldImagePath) as image:
        newJpgPath = os.path.join(outputDirectory, f"{fileName}.jpg")
        image.compression_quality = 99
        image.format = "jpg"
        image.save(filename=newJpgPath)

    # Delete original BMP
    os.remove(oldImagePath)

def RoundDown(value):
    return int(float(value))