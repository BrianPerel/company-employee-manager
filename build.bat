@echo off

::
:: converts the python src code files to an exe (NOTE: RUN THIS BATCH FILE FROM THE WINDOWS EXPLORER FOLDER, otherwise the exe may be created an a different location)
::

echo creating Employee_Manager.exe...
pyinstaller --noconsole --onefile %~dp0/src/GUI.py %~dp0/src/Employee_Management_System.py --icon=%~dp0/res/icon.ico --name EmployeeManager.exe
del "EmployeeManager.exe.spec" /q 
echo BUILD SUCCESSFUL
pause