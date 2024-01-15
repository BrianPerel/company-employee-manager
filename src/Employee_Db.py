'''
Author @ Brian Perel
GUI Employee Management System using XAMPP and mysql-connector module
* Python UI program that will store information about employees in a company using a dictionary with add, remove, update, look up operations
* Uses an employee class to set and get employee attributes
* Program requires user to start XAMPP control panel (Apache server (to be able to reach phpadmin website)
and MySQL (to be able to connect and perform database actions) modules)
'''

from tkinter.constants import DISABLED, NORMAL
import Employee_Management_System as EMS
import tkinter.messagebox as messagebox
from tzlocal import get_localzone
from datetime import datetime
import re as regular_exp
import mysql.connector
import webbrowser
import logging
import pickle
import sys
import os

class Employee_Db:

    # print(__doc__)
    def __init__(self, SAVED_EMPLOYEES_DATA_FILE, logger, xampp, employees):
        self.SAVED_EMPLOYEES_DATA_FILE = SAVED_EMPLOYEES_DATA_FILE
        self.employees = employees
        self.logger = logger
        self.xampp = xampp

        self.logger = logging.getLogger(__name__)

        self.__start_db_connection()

    def __start_db_connection(self):
        ''' actions to create and start the db connection
        '''

        # connect to the MySQL database using user credentials
        try:
            self.mydb = mysql.connector.connect(host='localhost', port=3306, autocommit=True, charset='utf8mb4', user='root')
        except mysql.connector.Error as err:
            self.logger.error('Exception caught: ' + str(err) + '\nTerminating xampp control panel and application')
            self.xampp.terminate()
            sys.exit()

        # create the empty database, if it doesn't already exist
        try:
            # create a buffered cursor object for executing SQL queries on a MySQL database
            self.mycursor = self.mydb.cursor(buffered=True)
            self.mycursor.execute('CREATE DATABASE IF NOT EXISTS company')
            self.mycursor.execute('USE company') # use company db
            self.logger.info('Database connection established to "company" using username "root"')
        except mysql.connector.Error as err:
            self.logger.error('Error while creating the database: ' + str(err))

    def close_app(self, main_window):
        ''' performs actions when closing the app
        '''

        connection_closed = False

        # close MySQL connection if one exists
        try:
            if self.mydb is not None:
                self.mycursor.close()
                self.mydb.close()
                connection_closed = True
        except mysql.connector.Error:
            self.logger.error('Error closing db connection')

        # close XAMPP app
        self.xampp.terminate()

        # close gui window
        main_window.destroy()

        if connection_closed:
            self.logger.info('Employee application, company database connection, and xampp module successfully closed')

    def check_db_size(self, gui):
        ''' attempts a select query on the db table to check if the database is empty. If we can't connect to the db because
            it doesn't yet exist or if the table is empty then start the GUI with these buttons disabled
        '''

        try:
            self.mycursor.execute('SELECT * FROM employees')
            rows = self.mycursor.fetchall()

            if(len(rows)) == 0:
                gui.reset_button['state'] = gui.delete_emp_button['state'] = gui.update_emp_button['state'] = gui.look_up_emp_button['state'] = DISABLED

                if(os.path.isfile(self.SAVED_EMPLOYEES_DATA_FILE) and os.access(self.SAVED_EMPLOYEES_DATA_FILE, os.W_OK)):
                    os.remove(self.SAVED_EMPLOYEES_DATA_FILE)

        except mysql.connector.Error:
                gui.reset_button['state'] = gui.delete_emp_button['state'] = gui.update_emp_button['state'] = gui.look_up_emp_button['state'] = DISABLED
                if(os.path.isfile(self.SAVED_EMPLOYEES_DATA_FILE) and os.access(self.SAVED_EMPLOYEES_DATA_FILE, os.W_OK)):
                    os.remove(self.SAVED_EMPLOYEES_DATA_FILE)

    def open_db_website(self):
        try:
            webbrowser.open('http://localhost/phpmyadmin/index.php?route=/sql&server=1&db=company&table=employees', new=1)
        except webbrowser.Error:
            self.logger.error("Failed to open DB website.")

    def look_up_employee(self, gui):
        ''' actions performed for when looking up an employee
        '''

        # function to look up an employee's info in dictionary, by the ID attained from GUI
        # Get an employee ID number to look up.
        ID = gui.id_output_entry.get()

        # ternary operator
        message = self.employees.get(ID) if (ID in self.employees) else 'No employee found under this ID'

        # create a showinfo message box
        messagebox.showinfo(title='Employee Info', message=str(message))

        gui.clear_gui_entry_fields()

    def add_employee(self, gui, check=True, work_type=''):
        ''' actions for when adding an employee, add an employee to dictionary, by info gathered from GUI
        '''
        self.mycursor.execute('CREATE TABLE IF NOT EXISTS employees (Employee_Creation_Date VARCHAR(50), ID INT UNSIGNED NOT NULL PRIMARY KEY, \
                            Name VARCHAR(12), Department VARCHAR(12), \
                            Title VARCHAR(12), Pay_Rate VARCHAR(6), \
                            Phone_Number VARCHAR(12), \
                            Work_Type VARCHAR(12))')

        try:
            date = str(datetime.now(get_localzone()).strftime("%m-%d-%Y %I:%M %p %Z")) # obtain current date and time and format it to be mm/dd/yyyy hh:tt am or pm
            ID = gui.id_output_entry.get()
            name = gui.name_output_entry.get().title().strip()
            dept = gui.dept_output_entry.get().title().strip()
            title = gui.job_title_output_entry.get().title().strip()
            pay_rate = gui.pay_rate_output_entry.get().strip()
            phone_number = gui.phone_num_output_entry.get().strip()
        except ValueError as err:
            self.logger.error('Exception caught: ' + str(err))
            check = False

        if ID == 'Enter id...' or name == 'Enter name...' or dept == 'Enter dept...' or \
        title == 'Enter title...' or pay_rate == 'Enter pay...' or phone_number == 'XXX-XXX-XXXX' or \
        not ID.isdigit() or len(pay_rate) == 0 or gui.radio_var.get() == 0:
            check = False

        # if user entered phone number without including dashes, manually attach them
        if '-' not in phone_number:
            phone_number = '{}-{}-{}'.format(phone_number[:3], phone_number[3:6], phone_number[6:])

        formatted_phone_number_without_dashes = "".join((phone_number[:3], phone_number[4:7], phone_number[8:])).replace(" ", "")

        for digit in formatted_phone_number_without_dashes:
            if not digit.isdigit():
                check = False
                break

        # use regular expressions to check format of info given
        # name, dept, title should all only contain letters, if nums are contained then mark
        pattern1 = regular_exp.match('^[a-zA-Z]+$', name)
        pattern2 = regular_exp.match('^[a-zA-Z]+$', dept)
        pattern3 = regular_exp.match('^[a-zA-Z]+$', title)
        name_has_digit = any(digit.isdigit() for digit in name)
        dept_has_digit = any(digit.isdigit() for digit in dept)
        title_has_digit = any(digit.isdigit() for digit in title)

        # make sure pay_rate field only accepts numbers
        pay_rate_has_letters = any(digit.isalpha() for digit in pay_rate)

        # add a $ to pay_rate before adding it to the database table
        if '$' in pay_rate:
            pay_rate = pay_rate.replace('$', '')

        try:
            # cast to float and format number, cast pay_rate back to string
            if not pay_rate_has_letters and float(pay_rate) > 0:
                pay_rate = '$' + str(format(float(pay_rate), '.2f'))
            else:
                check = False
        except ValueError as err:
            messagebox.showinfo(title='Validation Error', message='Couldn\'t add employee.')
            gui.clear_gui_entry_fields()
            return

        # value of 1 stands for part-time radio button option, 2 for full time option
        if gui.radio_var.get() == 1:
            work_type = 'Part time'
        elif gui.radio_var.get() == 2:
            work_type = 'Full time'

        # create instance and send the values
        new_emp = EMS.Employee_Management_System(ID, name, dept, title, pay_rate, phone_number, work_type)

        message_title = 'Validation Error'
        message = 'Couldn\'t add employee.'

        # conditional statement to add employee into dictionary
        if ID not in self.employees and len(phone_number) == 12 and check and len(ID) == 6 \
           and '' not in [name, dept, title, pay_rate, phone_number, work_type] \
           and pattern1 and pattern2 and pattern3 and not name_has_digit \
           and not dept_has_digit and not title_has_digit and ID != '000000' and phone_number != '000-000-0000':
            self.employees[ID] = new_emp
            message = 'The new employee has been added'

            # if db exists with at least 1 record in the table then enable these buttons
            gui.reset_button['state'] = gui.delete_emp_button['state'] = gui.update_emp_button['state'] = gui.look_up_emp_button['state'] = NORMAL

            # serialize the object
            file_obj = open(self.SAVED_EMPLOYEES_DATA_FILE, 'ab')
            pickle.dump(new_emp, file_obj)
            file_obj.close()

            # insert data into db table
            try:
                self.mycursor.execute('INSERT INTO employees (Employee_Creation_Date, ID, Name, Department, Title, \
                Pay_Rate, Phone_Number, Work_Type) values (%s, %s, %s, %s, %s, %s, %s, %s)',
                (date, ID, name, dept, title, pay_rate, phone_number, work_type))
            except mysql.connector.Error as err:
                message = 'An employee with that ID already exists.'
                gui.clear_gui_entry_fields()
                self.logger.error('Exception caught: ' + str(err))

        elif ID in self.employees:
            message = 'An employee with that ID already exists.'
            message_title='Success'

        # show info message box with data
        messagebox.showinfo(title=message_title, message=message)

        gui.clear_gui_entry_fields()

    def update_employee(self, gui, check=True, message='', work_type = ''):
        ''' actions performed to update an employee's data in the app by attaining info from GUI and
            updating an already existing employee's info in the dictionary
        '''

        self.mycursor.execute('CREATE TABLE IF NOT EXISTS employees (Employee_Creation_Date VARCHAR(30), ID INT UNSIGNED NOT NULL PRIMARY KEY, \
                            Name VARCHAR(12), Department VARCHAR(12), \
                            Title VARCHAR(12), Pay_Rate VARCHAR(6), \
                            Phone_Number VARCHAR(12), \
                            Work_Type VARCHAR(12))')

        # get values from entry box widget
        try:
            ID = gui.id_output_entry.get()
        except ValueError as err:
            self.logger.error('Exception caught: ' + str(err))
            check = False

        if ID in self.employees:
            name = gui.name_output_entry.get().title().strip()
            dept = gui.dept_output_entry.get().title().strip()
            title = gui.job_title_output_entry.get().title().strip()
            pay_rate = gui.pay_rate_output_entry.get().strip()
            phone_number = gui.phone_num_output_entry.get().strip()

            # if user entered phone number without including dashes, manually attach them
            if '-' not in phone_number:
                phone_number = '{}-{}-{}'.format(phone_number[:3], phone_number[3:6], phone_number[6:])

            formatted_phone_number_without_dashes = "".join((phone_number[:3], phone_number[4:7], phone_number[8:])).replace(" ", "")

            for digit in formatted_phone_number_without_dashes:
                if not digit.isdigit():
                    check = False
                    break

            # use regular expressions to check format of info given
            # name, dept, title should all only contain letters, if nums are contained then mark
            pattern1 = regular_exp.match('[a-zA-Z]+', name)
            pattern2 = regular_exp.match('[a-zA-Z]+', dept)
            pattern3 = regular_exp.match('[a-zA-Z]+', title)
            name_has_digit = any(digit.isdigit() for digit in name)
            dept_has_digit = any(digit.isdigit() for digit in dept)
            title_has_digit = any(digit.isdigit() for digit in title)

            # make sure pay_rate field only accepts numbers
            pay_rate_has_letters = any(digit.isalpha() for digit in pay_rate)

            # add a $ to pay_rate before adding it to the database table
            if '$' in pay_rate:
                pay_rate = pay_rate.replace('$', '')

            try:
                # cast to float and format number, cast pay_rate back to string
                if not pay_rate_has_letters and float(pay_rate) > 0:
                    pay_rate = '$' + str(format(float(pay_rate), '.2f'))
                else:
                    check = False
            except ValueError as err:
                messagebox.showinfo(title='Validation Error', message='Couldn\'t update employee\'s info')
                gui.clear_gui_entry_fields()
                return

            # create radio buttons: 0 is representative of when neither is selected, 1 is for first circle, 2 is for second circle
            if gui.radio_var.get() == 0 or len(phone_number) != 12 or not check \
                or '' in [name, dept, title, pay_rate, phone_number] or not pattern1 \
                or name_has_digit or not pattern2 or dept_has_digit or not pattern3 \
                or title_has_digit or pay_rate_has_letters or phone_number == '000-000-0000':
                    messagebox.showinfo(title='Validation Error', message='Couldn\'t update employee\'s info')
                    gui.clear_gui_entry_fields()
                    return
            elif gui.radio_var.get() == 1:
                work_type = 'Part time'
            elif gui.radio_var.get() == 2:
                work_type = 'Full time'

            # store employee object in employee dictionary, the dictionary's key is the employee's ID
            self.employees[ID] = EMS.Employee_Management_System(ID, name, dept, \
                                    title, pay_rate, phone_number, work_type)

            self.mycursor.execute('SELECT * FROM employees WHERE ID = %s', (ID,))  # execute sql statement with above statement as arg
            self.mycursor.execute('UPDATE employees SET Name=%s, Department=%s, Title=%s, Pay_Rate=%s, Phone_Number=%s, Work_Type=%s WHERE ID=%s',
                    (f'{name}', f'{dept}', f'{title}', f'{pay_rate}', f'{phone_number}', f'{work_type}', f'{ID}'))

            message = 'The employee has been updated'

        elif ID not in self.employees:
            message = 'No employee found under this ID'

        messagebox.showinfo(title='Info', message=message)

        gui.clear_gui_entry_fields()

    def delete_employee(self, gui):
        ''' deletes the employee from the app by locating it by ID in dictionary
        '''

        # get values from entry box widget
        ID = gui.id_output_entry.get()

        try:
            self.mycursor.execute('DELETE FROM employees WHERE ID = %s', (ID,))
        except mysql.connector.Error as err:
            self.logger.error('Exception caught: ' + str(err))

        # to delete an employee, must be in db. Perform this check
        if ID in self.employees:
            del self.employees[ID]
            message = 'Employee deleted'
        else:
            message = 'The specified ID number was not found'

        messagebox.showinfo(title='Info', message=message)

        gui.clear_gui_entry_fields()
        self.check_db_size(gui)

    def reset_system(self, gui):
        ''' actions performed to reset the app - deletes app memory, db, and .dat file
        '''

        if messagebox.askquestion(title='Reset System', message='Are you sure you want to delete everything in your employee database?') == 'yes':
            # function to reset app data, in case the company goes out of business. This will delete all data in app and the whole database
            self.employees = {}

            try:
                self.mycursor.execute('DROP TABLE IF EXISTS employees')

                if(os.path.isfile(self.SAVED_EMPLOYEES_DATA_FILE) and os.access(self.SAVED_EMPLOYEES_DATA_FILE, os.W_OK)):
                    os.remove(self.SAVED_EMPLOYEES_DATA_FILE)

                messagebox.showinfo(title='Success', message='System has been reset: database table and ' + self.SAVED_EMPLOYEES_DATA_FILE[3:] + ' deleted')
            except mysql.connector.Error as err:
                messagebox.showerror(title='Error', message='Database not found, file not found\n' + str(err))
            except FileNotFoundError as err:
                messagebox.showerror(title='Error', message='.dat data file not found\n' + str(err))

            gui.reset_button['state'] = gui.delete_emp_button['state'] = gui.update_emp_button['state'] = gui.look_up_emp_button['state'] = DISABLED

        gui.clear_gui_entry_fields()
