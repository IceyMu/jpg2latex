::@START python %~dp0\JpgToPdf.py
@echo off
cd %~dp0

:: Check for help option
for %%i in (%*) do (
    if -%%i- == --h- type help.txt & goto end
    if -%%i- == ---help- type help.txt & goto end
)

:: Pass arguments to Python script
python JpgToPdf.py %* || pause

:end
