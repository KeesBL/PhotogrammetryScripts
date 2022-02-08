# Notices
Write-Host ">>> Get Frames Fast w/ FFmpeg"
Write-Host ">>> Kees Beemster Leverenz, 2021"
Write-Host ""

# Get input video path
$inputFilePath = Read-Host -Prompt "Input video"
$inputFilePath = $inputFilePath -replace '"', ""

# Guard against invalid input path
$inputFilePathIsValid = Test-Path -Path $inputFilePath
if(-Not $inputFilePathIsValid)
{
	Write-Host "Input video path is invalid.  Script will exit in 3 seconds."
	Start-Sleep -s 3
	Exit
}

# Get output folder path
$outputFolderPath = Read-Host -Prompt "Output folder path"
$outputFolderPath = $outputFolderPath -replace '"', ""

# Guard against invalid outputFolderPath
$outputFolderPathIsValid = Test-Path -Path $outputFolderPath
if(-Not $outputFolderPathIsValid)
{
	Write-Host "Output folder path is invalid.  Script will exit in 3 seconds."
	Start-Sleep -s 3
	Exit
}

# Get framerate
$frameRate = Read-Host -Prompt "Input frame rate (number of frames to extract per second)"

# Determine outputFileName
$outputFileName = [System.IO.Path]::GetFileNameWithoutExtension($inputFilePath) + "__Frame_%0000d.bmp"
$outputFileNameTemplate = Join-Path -Path $outputFolderPath -ChildPath $outputFileName

# Create command
$command = "ffmpeg -i `"{0}`" -filter:v fps=fps={1} `"{2}`"" -f $inputFilePath, $frameRate, $outputFileNameTemplate
Write-Host $command

# Run command
Invoke-Expression $command
Write-Host "Done. Closing in 10 seconds..."
Start-Sleep -s 10
