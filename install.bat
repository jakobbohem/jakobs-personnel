REM # install.bat script for Windows env access to lookup.py

@echo off

:: Retrieve the current user PATH
for /f "tokens=2* delims= " %%a in ('"reg query HKCU\Environment /v PATH 2>nul | findstr /c:PATH"') do set CUR_PATH=%%b

:: Update the PATH
if defined CUR_PATH (
    setx PATH "%CUR_PATH%;%~dp0"
) else (
    setx PATH "%~dp0"
)


:done
echo Updated user PATH with script path