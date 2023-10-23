# Copy Python files from the root folder of this file to the Agisoft startup scripts folder
Write-Host "Copying scripts..."
$source = $PSScriptRoot
$dest = Join-Path $env:USERPROFILE -ChildPath '\AppData\Local\Agisoft\Metashape Pro\scripts'
$files = Get-ChildItem $source -File -include '*.py' -Recurse
Copy-Item -Path $files -Destination $dest
Write-Host "Scripts copied!" -ForegroundColor Green

# Install packages
Start-Process -Wait -NoNewWindow -FilePath "$Env:ProgramFiles\Agisoft\Metashape Pro\Python\Python.exe" -ArgumentList "-m pip install pillow"
Start-Process -Wait -NoNewWindow -FilePath "$Env:ProgramFiles\Agisoft\Metashape Pro\Python\Python.exe" -ArgumentList "-m pip install opencv-python"
Start-Process -Wait -NoNewWindow -FilePath "$Env:ProgramFiles\Agisoft\Metashape Pro\Python\Python.exe" -ArgumentList "-m pip install ffmpeg-python"
Start-Process -Wait -NoNewWindow -FilePath "$Env:ProgramFiles\Agisoft\Metashape Pro\Python\Python.exe" -ArgumentList "-m pip install wand"

# Note completion
Write-Host "Update complete! Restart Metashape." -ForegroundColor Green
Write-Host "Script will close in 3 seconds."
Start-Sleep -Seconds 3