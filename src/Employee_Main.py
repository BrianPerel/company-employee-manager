import Employee_Management_System as EMS
import tkinter.messagebox as messagebox
import Employee_Logger as EMS_Logger
from Employee_Db import Employee_Db
import Employee_Gui as EMS_Gui
from datetime import datetime
import subprocess
import psutil
import pickle
import time
import glob
import os

class Employee_Main:

    def start_app(self):
        # defines the file to save the apps employee profiles to. The saved file can be loaded later and will contain the current date
        self.SAVED_EMPLOYEES_DATA_FILE = f'..\\employees.{datetime.now().strftime("%m_%d_%Y")}.dat'
        self.logger = EMS_Logger.Employee_Logger.setup_custom_logger(self)

        self.employees = {} # create empty dictionary
        successful_launch = self.__start_xampp()

        if successful_launch:
            db = Employee_Db(self.SAVED_EMPLOYEES_DATA_FILE, self.logger, self.xampp, self.employees)

            try:
                # create a new file only if file doesn't already exist under the specific format
                if not any(glob.glob("..\\employees.*.dat")) and not os.path.isfile(self.SAVED_EMPLOYEES_DATA_FILE):
                    # create a new binary file to store binary object info, if one doesn't already exist in folder
                    file_obj = open(self.SAVED_EMPLOYEES_DATA_FILE, 'wb')
                    file_obj.close()
                else:
                    self.__load_file()
            except FileNotFoundError as e:
                self.logger.error(f"An error occurred: {e}")

            EMS_Gui.Employee_Gui(self.logger, db)

    def __start_xampp(self):
        # start XAMPP control panel using the subprocess module

        if self.__is_process_running('xampp-control.exe'):
            self.logger.error('An instance of XAMPP Control Panel is already running. Please close it before starting the application')
            return False
        else:
            try:
                self.xampp = subprocess.Popen('C:\\xampp\\xampp-control.exe')
                self.logger.info("XAMPP control panel started")
            except FileNotFoundError:
                self.logger.error("XAMPP control panel executable file not found")
                return False
            except PermissionError:
                self.logger.error("Insufficient permissions to execute XAMPP control panel")
                return False
            except subprocess.CalledProcessError as e:
                self.logger.error(f"Error starting XAMPP control panel: {e}")
                return False

            self.logger.info('Starting XAMPP Apache and MySQL modules...')

            # wait 2 seconds after launching XAMPP to make sure that Apache and MySQL services
            # started if user has auto launch enabled in XAMPP config.
            # This is to ensure that later when we attempt to connect to the
            # database the service had enough time to start before doing this
            time.sleep(2)

            # Apache and MySQL process names in XAMPP
            if self.__is_process_running('httpd.exe') and self.__is_process_running('mysqld.exe'):
                self.logger.info("XAMPP Apache and MySQL modules working correctly")
            else:
                self.logger.error("Unable to successfully start XAMPP Apache or MySQL module")
                self.xampp.terminate()
                return False

            return True

    def __is_process_running(self, process_name):
        return any(process.info['name'] == process_name for process in psutil.process_iter(['pid', 'name']))

    def __load_file(self):
        ''' actions performed for when loading the .dat binary data file into the app. Data is automatically saved from the last time app is used
        '''

        # get a list of all files in the parent directory
        dat_files_in_parent = os.listdir(os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir)))

        # find the first file with a .dat extension, then since it's in the parent directory prepend the ..\\
        self.SAVED_EMPLOYEES_DATA_FILE = "..\\"  + next((file for file in dat_files_in_parent if file.startswith("employees") and file.endswith(".dat")), None)

        try:
            # only attempt to open the data file if the file has read permission and is not empty
            if os.access(self.SAVED_EMPLOYEES_DATA_FILE, os.R_OK) and os.stat(self.SAVED_EMPLOYEES_DATA_FILE).st_size != 0:
                file_obj = open(self.SAVED_EMPLOYEES_DATA_FILE, 'rb')

                while True:
                    try:
                        # obtain the next (or first) object (employee) of the data file
                        content = pickle.load(file_obj)

                        ID = content.get_id_number()
                        if ID not in self.employees:
                            self.employees[ID] = EMS.Employee_Management_System(ID, content.get_name(), content.get_department(),
                                     content.get_title(), content.get_pay_rate(),
                                     content.get_phone_number(), content.get_work_type())

                    except EOFError as err:
                        break

                file_obj.close()

        except FileNotFoundError as err:
            messagebox.showerror(title='Info', message='File not found\n' + str(err))

# create instance of EMSGui class
app = Employee_Main()
app.start_app()