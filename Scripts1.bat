@echo off
setlocal enabledelayedexpansion

rem Set the directory where your Python scripts are located
set "script_dir=C:\Users\HP\Desktop\GS"

rem Define each script separately
set "script1=GS_download_TLE_prompt.py"
set "script2=GS_Spacetrack_satcat.py"
set "script3=GS_Spacetrack_TIP.py"
set "script4=GS_Spacetrackconjunction.py"
set "script5=GS_Spacetrackdecay.py"
set "script6=GSdownloadtle_CSV.py"

rem Number of scripts
set "script_count=6"

rem Display the script options
echo Select a script to run:
echo 1) %script1%
echo 2) %script2%
echo 3) %script3%
echo 4) %script4%
echo 5) %script5%
echo 6) %script6%


rem Get user input
set /p choice=Enter your choice (1-%script_count%): 

rem Validate input
if %choice% lss 1 goto invalid_choice
if %choice% gtr %script_count% goto invalid_choice

rem Retrieve the script name based on user choice
set "script=!script%choice%!"

rem Construct the full script path
set "script_path=%script_dir%\%script%"

echo Running: "%script_path%"
python "%script_path%"
goto end

:invalid_choice
echo Invalid choice. Exiting.

:end
endlocal
pause
