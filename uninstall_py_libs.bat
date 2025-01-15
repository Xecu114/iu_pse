@echo off

REM 1. Uninstall packages
pip uninstall pyqt6
pip uninstall PyQt6-Charts
pip uninstall pygame

REM 2. Done
echo ----------------------------------------
echo Unintallation completed.
echo Press any key to exit...
echo ----------------------------------------
pause >nul