import AddPhotosFromFolderRecursive
import RelocatePhotosRecursive
import NewChunkFromSelection
import CountEnabledCameras
import RemoveDisabledCameras
import SortIntoFolders
import RenamePhotosInPlace
import ExtractFramesFast
import VerifyImagesInDirectory
import DisableEveryOtherCamera
import DeduplicateCamerasPrioritizeUnaligned
import AddNewPhotosFromFolder

# This script creates a custom menu of
# from utility scripts in Metashape.
# 
# Kees Beemster Leverenz 2024

# General scripts
Metashape.app.addMenuItem("Custom/Add Photos from Folder (Recursive)", AddPhotosFromFolderRecursive.AddPhotosFromFolderRecursive)
Metashape.app.addMenuItem("Custom/Relocate Photos in Folder (Recursive)", RelocatePhotosRecursive.RelocatePhotosRecursive)
Metashape.app.addMenuItem("Custom/Add New Photos from Folder", AddNewPhotosFromFolder.AddNewPhotosFromFolder)
Metashape.app.addMenuSeparator("Custom")

Metashape.app.addMenuItem("Custom/Create New Chunk from Selection", NewChunkFromSelection.NewChunkFromSelection)
Metashape.app.addMenuItem("Custom/Count Enabled Cameras", CountEnabledCameras.CountEnabledCameras)
Metashape.app.addMenuItem("Custom/Remove Disabled Cameras", RemoveDisabledCameras.PromptUserToRemove)
Metashape.app.addMenuItem("Custom/Disable Every Other Camera", DisableEveryOtherCamera.DisableEveryOtherCamera)
Metashape.app.addMenuItem("Custom/Deduplicate Cameras (Prioritize Unaligned)", DeduplicateCamerasPrioritizeUnaligned.DeduplicateCamerasPrioritizeUnaligned)
Metashape.app.addMenuSeparator("Custom")

# Organize
Metashape.app.addMenuItem("Custom/Organize/Sort Into Folders by Date and Photographer", SortIntoFolders.SortIntoFolders)
Metashape.app.addMenuItem("Custom/Organize/Rename Photos in Place", RenamePhotosInPlace.RenamePhotosInPlace)

# Video Tools
Metashape.app.addMenuItem("Custom/Video Tools/Extract Frames Fast", ExtractFramesFast.ExtractFramesFast_Ffmpeg)

# Image Tools
Metashape.app.addMenuItem("Custom/Image Tools/Verify Images in Folder", VerifyImagesInDirectory.VerifyImagesInDirectory)
