@ECHO OFF
ECHO creating Employee_Manager.exe...
pyinstaller --noconsole --onefile %~dp0/src/GUI.py %~dp0/src/Employee_Management_System.py --icon=%~dp0/res/icon.ico --name EmployeeManager.exe
del "EmployeeManager.exe.spec" /q 
ECHO BUILD SUCCESSFUL
PAUSE