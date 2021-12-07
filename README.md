# Company-employee-program
About: Python program that will store information about employees in a company using a dictionary. 

NOTE: The app will require you to have xampp installed on your machine under the path 'C:\xampp'. 
You will need to open the xampp control panel and have Apache and MySQL running before you run the app. 

NOTE: You must set xampp to auto start the apache and mysql services

NOTE: In http://localhost/phpmyadmin/index.php under user accounts tab you will need to create a user 
account that matches the account listed in src code 

NOTE: you must have Python's mysql connector module installed to do dev. work
-if not run the cmds 'pip install mysql-connector-python'

To create .exe: Use these cmds in cmd prompt to generate a .exe binary file of the application
pyinstaller must be installed in cmd prompt to run 
the following cmd (if not installed use 'pip install pyinstaller')
pyinstaller --noconsole --onefile GUI.py --icon=res/icon.ico --name App

or alternatively you can delete the build and dist folders + run the build.bat file, but run it from the windows explorer location of this project

[Check out the project here](https://brianperel.github.io/project2.htm)
