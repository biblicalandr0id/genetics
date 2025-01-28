@echo off
echo Starting conception process...

:: Create necessary directories
if not exist embryos mkdir embryos
if not exist conception_records mkdir conception_records
if not exist development_logs mkdir development_logs

:: Run conception process
python conception.py > temp_conception.txt
set /p EMBRYO_ID=<temp_conception.txt
del temp_conception.txt

:: Generate the embryo file
python embryo_generator.py %EMBRYO_ID%

echo.
echo Conception complete!
echo New embryo created in embryos folder
echo Conception record saved in conception_records folder
echo.
echo Press any key to exit...
pause > nul
