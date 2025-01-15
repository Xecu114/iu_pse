@echo off

REM 1. Install packages
pip install --upgrade pip
pip install pyqt6
pip install PyQt6-Charts
pip install pygame

REM 2. Done
echo ----------------------------------------
echo Installation completed.
echo Press any key to exit...
echo ----------------------------------------
pause >nul