::@START python %~dp0\JpgToPdf.py
@echo off

:: Check for help option
for %%i in (%*) do (
    if -%%i- == --h- type %~dp0\help.txt & goto end
    if -%%i- == ---help- type %~dp0\help.txt & goto end
)

:: Pass arguments to Python script
python %~dp0\JpgToPdf.py %* || pause

:end
