### company-employee-manager
- About: Python program that will store information about employees in a company using a dictionary.
- Python version `3.10` used for development

- The app will require you to have XAMPP installed on your machine under the path `C:\xampp`.
- You must set XAMPP config to auto start the Apache and MySQL services for the app to execute correctly

- The mysql database will be created by the app, we will use the default auto created admin user `root`
- A local backup .dat data file will be created and updated by the app

- To create the .exe: run the build.py script which will generate a new dist folder with the icon and exe files

- Before running the build.py file, you can optionally download the upx (Ultimate Packer for Executables) folder and put into the root of your local C drive. It will reduce the size of executable files, making them smaller and more efficient.
Download upx from here: https://github.com/upx/upx/releases/tag/v4.2.1

- Project external library dependencies: pyinstaller, tzlocal, mysql-connector-python. PyInstaller is the command-line tool used to package Python scripts/applications into standalone executables, run `pip install pyinstaller` in cmd to install. MySQL connector installed to do development work/ interact via driver with mysql databases. Run the command `pip install mysql-connector-python` to install. The tzlocal is utilized to obtain local timezones, run `pip install tzlocal`

- [Check out the project here](https://brianperel.github.io/project2.htm)
