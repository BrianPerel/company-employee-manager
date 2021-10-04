@ECHO OFF
ECHO creating Employee_Manager.exe...
pyinstaller --noconsole --onefile %~dp0/src/GUI.py %~dp0/src/Employee_Management_System.py --icon=%~dp0/res/icon.ico --name Employee_Manager.exe
del "Employee_Manager.exe.spec" /q 
ECHO BUILD SUCCESSFUL
PAUSE