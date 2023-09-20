@echo off
REM # install.bat script for Windows env access to lookup.py

set "SCRIPT_DIR=%~dp0"

:: Retrieve the current user PATH
for /f "tokens=2* delims= " %%a in ('"reg query HKCU\Environment /v PATH 2>nul | findstr /c:PATH"') do set CUR_PATH=%%b

:: Check if the script's directory is already in the PATH
echo %CUR_PATH% | find /I "%SCRIPT_DIR%" >nul
if errorlevel 1 (
    :: Update the PATH only if the script's directory is not already present
    if defined CUR_PATH (
        setx PATH "%CUR_PATH%;%~dp0"
    ) else (
        setx PATH "%~dp0"
    )
) else (
    echo Script directory is already in the PATH.
)

:done
echo Updated user PATH with %~dp0