@echo off

REM 1. Pakete installieren
pip install --upgrade pip
pip install pyqt6
pip install PyQt6-Charts
pip install pygame

REM 2. Fertig
echo ----------------------------------------
echo Installation abgeschlossen.
echo Druecke eine beliebige Taste zum Beenden...
echo ----------------------------------------
pause >nul