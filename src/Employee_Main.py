import Employee_Management_System as EMS
import tkinter.messagebox as messagebox
import Employee_Logger as EMS_Logger
import Employee_Gui as EMS_Gui
import Employee_Db as EMS_Db
from datetime import datetime
import subprocess
import logging
import psutil
import pickle
import time
import glob
import os

'''
Author @ Brian Perel
GUI Employee Management System using XAMPP and mysql-connector module
* Python UI program that will store information about employees in a company using a dictionary with add, remove, update, and look up operations
* Uses an employee class to set and get the employee attributes
* Program requires user to start XAMPP control panel (Apache http server (to be able to reach phpadmin website)
and MySQL (to be able to connect and perform database actions) modules)
'''

class Employee_Main:

    def __init__(self):
        # defines the file to save the apps employee profiles to. The saved file can be loaded later and will contain the current date
        self.SAVED_EMPLOYEES_DATA_FILE = f'..\\employees.{datetime.now().strftime("%m_%d_%Y")}.dat'
        self.logger = EMS_Logger.Employee_Logger.setup_custom_logger(self)

        self.logger = logging.getLogger(__name__)

        self.employees = {} # create empty dictionary
        successful_launch = self.__start_xampp()

        if successful_launch:
            try:
                # create a new file only if file doesn't already exist under the specific format
                if not any(glob.glob("..\\employees*.dat")) and not os.path.isfile(self.SAVED_EMPLOYEES_DATA_FILE):
                    # create a new binary file to store binary object info, if one doesn't already exist in folder
                    file_obj = open(self.SAVED_EMPLOYEES_DATA_FILE, 'wb')
                    file_obj.close()

                    self.logger.info('An existing dat file could not be found')
                    self.logger.info(self.SAVED_EMPLOYEES_DATA_FILE + ' file has been created')
                else:
                    self.__load_file()
            except FileNotFoundError as e:
                self.logger.error(f"An error occurred while loading .dat file: {e}")

            EMS_Gui.Employee_Gui(EMS_Db.Employee_Db(self.SAVED_EMPLOYEES_DATA_FILE, self.xampp, self.employees))

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
                self.logger.info("XAMPP Apache and MySQL modules are working correctly")
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

        if dat_files_in_parent is not None:
            log_file = next((file for file in dat_files_in_parent if file.startswith("employees") and file.endswith(".dat")), None)

            if log_file is not None:
                # find the first file with a .dat extension, then prepend "..\\" if found
                self.SAVED_EMPLOYEES_DATA_FILE = "..\\"  + log_file
                self.logger.info('Existing dat file found, using ' + self.SAVED_EMPLOYEES_DATA_FILE)

        try:
            # only attempt to open the data file if the file has read permission and is not empty
            if os.access(self.SAVED_EMPLOYEES_DATA_FILE, os.R_OK) and os.stat(self.SAVED_EMPLOYEES_DATA_FILE).st_size != 0:
                with open(self.SAVED_EMPLOYEES_DATA_FILE, 'rb') as file_obj:

                    while True:
                        try:
                            # obtain the first or next object (employee) of the data file
                            content = pickle.load(file_obj)

                            ID = content.get_id_number()
                            if ID not in self.employees:
                                self.employees[ID] = EMS.Employee_Management_System(ID, content.get_name(), content.get_department(),
                                         content.get_title(), content.get_pay_rate(),
                                         content.get_phone_number(), content.get_work_type())

                        except EOFError as err:
                            break

        except FileNotFoundError as err:
            messagebox.showerror(title='Info', message='File not found\n' + str(err))

# create an instance of Main Employee class to start the app
Employee_Main()