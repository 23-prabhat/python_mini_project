@echo off
set "TOOL_DIR=%~dp0"
echo Setting up Git Conflict Resolver (gcr) for Windows...

:: 1. Create gcr.bat shim in the tool directory
echo @echo off > "%TOOL_DIR%gcr.bat"
echo python "%%~dp0main.py" %%* >> "%TOOL_DIR%gcr.bat"

:: 2. Add the tool directory to the user's PATH permanently
setx PATH "%PATH%;%TOOL_DIR%"

echo.
echo ╔══════════════════════════════════════════════════════╗
echo ║ SUCCESS: Git Conflict Resolver (gcr) is installed!  ║
echo ╚══════════════════════════════════════════════════════╝
echo.
echo How to use:
echo   1. RESTART your terminal (Command Prompt, PowerShell, or Windows Terminal).
echo   2. Navigate to any Git repository with merge conflicts.
echo   3. Run 'gcr --all' to resolve everything.
echo   4. Run 'gcr filename' to resolve a specific file.
echo.
echo Installation Directory: %TOOL_DIR%
echo Command Name: gcr
echo.
pause
