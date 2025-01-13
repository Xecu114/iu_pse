@echo off

REM 1. Pakete deinstallieren
pip uninstall pyqt6
pip uninstall PyQt6-Charts
pip uninstall pygame

REM 2. Fertig
echo ----------------------------------------
echo Deinstallation abgeschlossen.
echo Druecke eine beliebige Taste zum Beenden...
echo ----------------------------------------
pause >nul