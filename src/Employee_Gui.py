'''
Author @ Brian Perel
GUI Employee Management System using XAMPP and mysql-connector module
-> Python UI program that will store information about employees in a company using a dictionary with add, remove, update, look up operations
-> Uses an employee class to set and get employee attributes
-> Program requires user to start XAMPP control panel (Apache server (to be able to reach phpadmin website)
and MySQL (to be able to connect and perform database actions) modules)
'''

from tkinter.constants import DISABLED, NORMAL
import Employee_Management_System as EMS
import tkinter.messagebox as messagebox
from tkinter import PhotoImage
from datetime import datetime
import re as regular_exp
import mysql.connector
import tkinter as tk
import subprocess
import webbrowser
import pickle
import time
import os

class EMSGui:

    # create the empty dictionary
    __employees = {}

    # print(__doc__)
    def __init__(self):
        self.__start_db_connection()
        self.__create_gui()

        self.__check_db_size()

        # create a new file only if file doesn't exist, otherwise don't
        if not os.path.isfile(SAVED_EMPLOYEES_DATA_FILE) and os.access(SAVED_EMPLOYEES_DATA_FILE, os.R_OK):
            # create a new binary file to store binary object info, if one doesn't already exist in folder
            file_obj = open(SAVED_EMPLOYEES_DATA_FILE, 'wb')
            file_obj.close()
        else:
            self.__load_file()

    def __create_gui(self):
        ''' create and place main gui window, buttons, labels, entry's, and a canvas1 line '''

        self.main_window = tk.Tk()  # make the GUI window
        self.main_window.geometry('520x420')  # width x height of the GUI window

        try:
            self.main_window.iconphoto(True, PhotoImage(file='../res/icon.png'))
        except Exception as e:
            print(f"An error occurred: {e}")

        self.main_window.configure(background='lightgrey')  # app (GUI) background color
        self.main_window.title('EMS')  # app title
        self.main_window.resizable(0, 0)  # disable resizable option for GUI
        self.main_window.eval('tk::PlaceWindow . center')  # launches the GUI in the center of the screen

        # create a GUI label (display EMPLOYEE MANAGEMENT SYSTEM) = the header_label of the GUI app
        self.header_label = tk.Label(text='EMPLOYEE MANAGEMENT SYSTEM',
                    font='Times 12 bold', bg='lightgrey')

        # build line between header_label and the body of app
        self.canvas1 = tk.Canvas(self.main_window, width=495, height=40, bd=0,
                    borderwidth=0, bg='lightgrey', highlightthickness=0.5,
                    highlightbackground='lightgrey')

        # create line between header_label and body of app
        self.canvas1.create_line(2, 25, 800, 25, width=2)

        # GUI button 1
        self.look_up_emp_button = tk.Button(text='Look Up Employee',
                    command=self.__look_up_employee, bg='SystemButtonFace')

        # create StringVar variables to store value input into entry box widget
        self.output_entry_var1 = tk.StringVar()
        self.output_entry_var2 = tk.StringVar()
        self.output_entry_var3 = tk.StringVar()
        self.output_entry_var4 = tk.StringVar()
        self.output_entry_var5 = tk.StringVar()
        self.output_entry_var6 = tk.StringVar()

        # store input value from app into radio button variable
        self.radio_var = tk.IntVar()

        # GUI message displayed in window (Label)
        self.enter_id_label = tk.Label(text='\tID:', font=('Courier', 10), bg='lightgrey')

        # create an output box (GUI entry)
        self.id_output_entry = tk.Entry(width=15,
                    textvariable=self.output_entry_var1, font=('Courier', 10), bd=2,
                    highlightthickness=1, highlightcolor='black', validate="key",
                    validatecommand=(self.main_window.register(self.__validate_entry), '%P'))

        # sets focus on the first text field in app on startup
        self.id_output_entry.focus_set()

        # GUI button
        self.add_emp_button = tk.Button(text='Add New Employee', command=self.__add_employee)

        # create label
        self.enter_name_label = tk.Label(text='\tName:', font=('Courier', 10),
                                                               bg='lightgrey')

        # take entry box variable and perform action
        self.name_output_entry = tk.Entry(width=15,
                    textvariable=self.output_entry_var2, font=('Courier', 10), bd=2,
                    highlightthickness=1, highlightcolor='black', foreground='gray',
                    validate="key", validatecommand=(self.main_window.register(self.__validate_entry), '%P'))

        # GUI button (update employee)
        self.update_emp_button = tk.Button(text='Update Employee', command=self.__update_employee)

        self.enter_dept_label = tk.Label(text='\tDepartment:', font=('Courier', 10),
                                                       bg='lightgrey')

        # take entry box variable and perform action
        self.dept_output_entry = tk.Entry(width=15,
                    textvariable=self.output_entry_var3, font=('Courier', 10), bd=2,
                    highlightthickness=1, highlightcolor='black', foreground='gray',
                    validate="key", validatecommand=(self.main_window.register(self.__validate_entry), '%P'))

        # GUI buttons (delete employee)
        self.delete_emp_button = tk.Button(text='Delete Employee', command=self.__delete_employee)

        # display formatted label
        self.enter_title_label = tk.Label(text='\tTitle:', font=('Courier', 10),
                                          bg='lightgrey')

        # take entry box variable and perform action
        self.job_title_output_entry = tk.Entry(width=15,
                    textvariable=self.output_entry_var4, font=('Courier', 10), bd=2,
                    highlightthickness=1, highlightcolor='black', foreground='grey',
                    validate="key", validatecommand=(self.main_window.register(self.__validate_entry), '%P'))

        # Opens xampp's MySQL module's admin website via direct link
        self.visit_db_button = tk.Button(text='Visit DB website',
                    command=self.__open_db_website)

        # take entry box variable and perform action
        self.pay_rate_output_entry = tk.Entry(width=15,
                    textvariable=self.output_entry_var5, font=('Courier', 10), bd=2,
                    highlightthickness=1, highlightcolor='black', foreground='grey',
                    validate="key", validatecommand=(self.main_window.register(self.__validate_entry), '%P'))

        self.canvas1_2 = tk.Canvas(self.main_window, width=150, height=40, bd=0,
                    borderwidth=0, bg='lightgrey', highlightthickness=0.5,
                    highlightbackground='lightgrey')

        self.canvas1_2.create_line(2, 25, 600, 25, width=2)

        # display formatted label
        self.enter_pay_rate_label = tk.Label(text='\tPay Rate:', font=('Courier', 10), bg='lightgrey')

        # display formatted label
        self.enter_phone_num_label = tk.Label(text='\tPhone Number:', font=('Courier', 10), bg='lightgrey')

        self.phone_num_output_entry = tk.Entry(width=15,
                        textvariable=self.output_entry_var6, font=('Courier', 10), bd=2,
                        highlightthickness=1, highlightcolor='black', foreground='grey',
                        validate="key", validatecommand=(self.main_window.register(self.__validate_entry), '%P'))

        # GUI formatted buttons, call appropriate method when clicked
        self.reset_button = tk.Button(text='Reset System', command=self.__reset_system)

        # reset radio button variable to blank option (0)
        self.radio_var.set(0)

        # create radio button
        self.rb1 = tk.Radiobutton(text='Part Time Employee', variable=self.radio_var,
                                    bg='lightgrey', value=1, cursor='hand2')

        # create radio button
        self.rb2 = tk.Radiobutton(text='Full Time Employee', variable=self.radio_var,
                                    bg='lightgrey', value=2, cursor='hand2')

        buttons = [self.look_up_emp_button, self.add_emp_button, self.update_emp_button,
                   self.delete_emp_button, self.reset_button, self.visit_db_button]

        for button in buttons:
            button.config(font=('Courier', 10), borderwidth=3, cursor='hand2')
            button.bind('<Enter>', self.__on_hover)
            button.bind('<Leave>', self.__on_leave)

        # build line between body of app and footer_label
        self.canvas2 = tk.Canvas(self.main_window, width=495, height=40, bd=0,
                            borderwidth=0, bg='lightgrey', highlightthickness=0.5,
                            highlightbackground='lightgrey')

        # create line between body of app and footer_label
        self.canvas2.create_line(2, 25, 600, 25, width=2)

        # display formatted label in app
        self.footer_label = tk.Label(text='created by Brian Perel', font=('Courier', 10), bg='lightgrey')

        # make program position and display all gui components (widgets)
        self.header_label.place(x=120, y=2)
        self.canvas1.place(x=10, y=20)
        self.look_up_emp_button.place(x=10, y=65)
        self.enter_id_label.place(x=283, y=67)
        self.id_output_entry.place(x=380, y=67)
        self.add_emp_button.place(x=10, y=105)
        self.enter_name_label.place(x=267, y=107)
        self.name_output_entry.place(x=380, y=107)
        self.update_emp_button.place(x=10, y=145)
        self.enter_dept_label.place(x=220, y=147)
        self.dept_output_entry.place(x=380, y=147)
        self.delete_emp_button.place(x=10, y=185)
        self.enter_title_label.place(x=260, y=187)
        self.job_title_output_entry.place(x=380, y=187)
        self.enter_pay_rate_label.place(x=237, y=225)
        self.pay_rate_output_entry.place(x=380, y=227)
        self.enter_phone_num_label.place(x=205, y=265)
        self.phone_num_output_entry.place(x=380, y=267)
        self.rb1.place(x=240, y=307)
        self.rb2.place(x=380, y=307)
        self.visit_db_button.place(x=10, y=225)
        self.canvas1_2.place(x=10, y=258)
        self.reset_button.place(x=10, y=307)
        self.canvas2.place(x=10, y=340)
        self.footer_label.place(x=160, y=380)

        entries = [self.id_output_entry, self.name_output_entry, self.dept_output_entry, self.job_title_output_entry,
                   self.pay_rate_output_entry, self.phone_num_output_entry]

        for entry in entries:
            # if user clicks in this text field box with their mouse, call this function
            entry.bind('<Button-1>', self.__on_click)
            # if user clicks in this text field box with their keyboard, call this function
            entry.bind('<FocusIn>', self.__on_click)
            # if insertion pointer leaves current text field (focus is lost) call this function
            entry.bind('<FocusOut>', lambda event, entry=entry: self.__focus_out(event, entry))

        # listens for when 'x' exit button is pressed and routes to __close_app
        self.main_window.protocol('WM_DELETE_WINDOW', self.__close_app)

    def __validate_entry(self, value):
        # only allow up to 6 characters in ID and up to 4 characters in name
        if self.main_window.focus_get() == self.id_output_entry:
            return len(value) <= 6

        elif self.main_window.focus_get() in [self.name_output_entry, self.dept_output_entry,
                                              self.job_title_output_entry, self.phone_num_output_entry]:
            return len(value) <= 12

        elif self.main_window.focus_get() == self.pay_rate_output_entry:
            return len(value) <= 6

        else:
            return True

    def __start_db_connection(self):
        ''' actions to create and start the db connection
        '''

        # connect to the MySQL database using user credentials
        try:
            # host='localhost', port=3306
            self.mydb = mysql.connector.connect(
            host='localhost', port=3306, user='root')
        except mysql.connector.Error as err:
            print('Exception caught: ' + str(err))
            xampp.terminate()

        # create the empty database and table, if they don't already exist
        try:
            # create a buffered cursor object for executing SQL queries on a MySQL database
            self.mycursor = self.mydb.cursor(buffered=True)
            self.mycursor.execute('CREATE DATABASE IF NOT EXISTS employee_db')
            self.mycursor.execute('USE employee_db')
        except mysql.connector.Error as err:
            print('Error while creating the database or table: ' + str(err))

    def __open_db_website(self):
        try:
            webbrowser.open('http://localhost/phpmyadmin/index.php?route=/sql&server=1&db=employee_db&table=employees&pos=0', new=1)
        except webbrowser.Error:
            print("Failed to open DB website.")

    def __close_app(self):
        ''' performs actions when closing the app
        '''

        # close MySQL connection if one exists
        try:
            if self.mydb is not None:
                self.mycursor.close()
                self.mydb.close()
        except mysql.connector.Error:
            print('Error closing db connection')

        # close xampp app
        xampp.terminate()

        # close gui window
        self.main_window.destroy()

    def __check_db_size(self):
        ''' attempts a select query on the db table to check if the database is empty. If we can't connect to the db because
            it doesn't yet exist or if the table is empty then start the GUI with these buttons disabled
        '''

        try:
            self.mycursor.execute('SELECT * FROM employees')
            rows = self.mycursor.fetchall()

            if(len(rows)) == 0:
                self.reset_button['state'] = self.delete_emp_button['state'] = self.update_emp_button['state'] = self.look_up_emp_button['state'] = DISABLED
                if(os.path.isfile(SAVED_EMPLOYEES_DATA_FILE) and os.access(SAVED_EMPLOYEES_DATA_FILE, os.W_OK)):
                    os.remove(SAVED_EMPLOYEES_DATA_FILE)
        except mysql.connector.Error:
                self.reset_button['state'] = self.delete_emp_button['state'] = self.update_emp_button['state'] = self.look_up_emp_button['state'] = DISABLED
                if(os.path.isfile(SAVED_EMPLOYEES_DATA_FILE) and os.access(SAVED_EMPLOYEES_DATA_FILE, os.W_OK)):
                    os.remove(SAVED_EMPLOYEES_DATA_FILE)

    def __look_up_employee(self):
        ''' actions performed for when looking up an employee
        '''

        # function to look up an employee's info in dictionary, by the ID attained from GUI
        # Get an employee ID number to look up.
        ID = self.id_output_entry.get()

        # ternary operator
        message = self.__employees.get(ID) if (ID in self.__employees) else 'No employee found under this ID'

        # create a showinfo message box
        messagebox.showinfo(title='Employee Info', message=str(message))

        self.__clear_gui_entry_fields()

    def __add_employee(self, check=True, work_type=''):
        ''' actions for when adding an employee, add an employee to dictionary, by info gathered from GUI
        '''
        self.mycursor.execute('CREATE TABLE IF NOT EXISTS employees (Employee_Creation_Date VARCHAR(30), ID INT PRIMARY KEY, \
                            Name VARCHAR(30), Department VARCHAR(30), \
                            Title VARCHAR(30), Pay_Rate VARCHAR(30), \
                            Phone_Number VARCHAR(30), \
                            Work_Type VARCHAR(30))')

        try:
            date = str(datetime.now().strftime("%m-%d-%Y %I:%M %p")) # obtain current date and time and format it to be mm/dd/yyyy hh:tt am or pm
            ID = self.id_output_entry.get()
            name = self.name_output_entry.get().title().strip()
            dept = self.dept_output_entry.get().title().strip()
            title = self.job_title_output_entry.get().title().strip()
            pay_rate = self.pay_rate_output_entry.get().strip()
            phone_number = self.phone_num_output_entry.get().strip()
        except ValueError as err:
            print('Exception caught: ' + str(err))
            check = False

        if ID == 'Enter id...' or name == 'Enter name...' or dept == 'Enter dept...' or \
        title == 'Enter title...' or pay_rate == 'Enter pay...' or phone_number == 'XXX-XXX-XXXX' or \
        not ID.isdigit() or len(pay_rate) == 0 or self.radio_var.get() == 0:
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
        pattern1 = regular_exp.match('[a-zA-Z]+', name)
        pattern2 = regular_exp.match('[a-zA-Z]+', dept)
        pattern3 = regular_exp.match('[a-zA-Z]+', title)
        name_has_digit = any(digit.isdigit() for digit in name)
        dept_has_digit = any(digit.isdigit() for digit in dept)
        title_has_digit = any(digit.isdigit() for digit in title)

        # value of 1 stands for part-time radio button option, 2 for full time option
        if self.radio_var.get() == 1:
            work_type = 'Part time'
        elif self.radio_var.get() == 2:
            work_type = 'Full time'

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
            messagebox.showinfo(title='Info', message='Couldn\'t add employee.')
            self.__clear_gui_entry_fields()
            return

        # create instance and send the values
        new_emp = EMS.Employee_Management_System(ID, name, dept, title, pay_rate, phone_number, work_type)

        # conditional statement to add employee into dictionary
        if ID not in self.__employees and len(phone_number) == 12 and check and len(ID) == 6 \
           and '' not in [name, dept, title, pay_rate, phone_number, work_type] \
           and pattern1 and pattern2 and pattern3 and not name_has_digit \
           and not dept_has_digit and not title_has_digit:
            self.__employees[ID] = new_emp
            message = 'The new employee has been added'

            # if db exists with at least 1 record in the table then enable these buttons
            self.reset_button['state'] = self.delete_emp_button['state'] = self.update_emp_button['state'] = self.look_up_emp_button['state'] = NORMAL

            # serialize the object
            file_obj = open(SAVED_EMPLOYEES_DATA_FILE, 'ab')
            pickle.dump(new_emp, file_obj)
            file_obj.close()

            # insert data into db table
            try:
                self.mycursor.execute('INSERT INTO employees (Employee_Creation_Date, ID, Name, Department, Title, \
                Pay_Rate, Phone_Number, Work_Type) values (%s, %s, %s, %s, %s, %s, %s, %s)',
                (date, ID, name, dept, title, pay_rate, phone_number, work_type))

                self.mydb.commit() # commit the changes to the database
            except mysql.connector.Error as err:
                message = 'An employee with that ID already exists.'
                self.__clear_gui_entry_fields()
                print('Exception caught: ' + str(err))

        # input validation: make sure no fields are blank and input of proper lengths is given
        elif '' in [ID, name, dept, title, pay_rate, phone_number, work_type] \
             or not check or len(ID) != 6 or not pattern1 \
             or not pattern2 or not pattern3 or name_has_digit \
             or dept_has_digit or title_has_digit or (len(phone_number) != 12):
            message = 'Couldn\'t add employee.'
        elif ID in self.__employees:
            message = 'An employee with that ID already exists.'

        # show info message box with data
        messagebox.showinfo(title='Info', message=message)

        self.__clear_gui_entry_fields()

    def __update_employee(self, check=True, message='', work_type = ''):
        ''' actions performed to update an employee's data in the app by attaining info from GUI and
            updating an already existing employee's info in the dictionary
        '''

        # create the empty database and table
        self.mycursor.execute('CREATE TABLE IF NOT EXISTS employees (Employee_Creation_Date VARCHAR(30), ID INT PRIMARY KEY, \
                    Name VARCHAR(30), Department VARCHAR(30),\
                    Title VARCHAR(30), Pay_Rate VARCHAR(30), \
                    Phone_Number VARCHAR(30), \
                    Work_Type VARCHAR(30))')

        # get values from entry box widget
        try:
            ID = self.id_output_entry.get()
        except ValueError as err:
            print('Exception caught: ' + str(err))
            check = False

        if ID in self.__employees:
            name = self.name_output_entry.get().title().strip()
            dept = self.dept_output_entry.get().title().strip()
            title = self.job_title_output_entry.get().title().strip()
            pay_rate = self.pay_rate_output_entry.get().strip()
            phone_number = self.phone_num_output_entry.get().strip()

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
                messagebox.showinfo(title='Info', message='Couldn\'t update employee\'s info')
                self.__clear_gui_entry_fields()
                return

            # create radio buttons: 0 is representative of when neither is selected, 1 is for first circle, 2 is for second circle
            if self.radio_var.get() == 0 or len(phone_number) != 12 or not check \
            or '' in [name, dept, title, pay_rate, phone_number] or not pattern1 \
            or name_has_digit or not pattern2 or dept_has_digit or not pattern3 \
            or title_has_digit or pay_rate_has_letters:
                messagebox.showinfo(title='Info', message='Couldn\'t update employee\'s info')
                self.__clear_gui_entry_fields()
                return
            elif self.radio_var.get() == 1:
                work_type = 'Part time'
            elif self.radio_var.get() == 2:
                work_type = 'Full time'

            # store employee object in employee dictionary, the dictionary's key is the employee's ID
            self.__employees[ID] = EMS.Employee_Management_System(ID, name, dept, \
                                    title, pay_rate, phone_number, work_type)

            check = 'SELECT * FROM employees WHERE ID = %s'
            self.mycursor.execute(check, (ID,))  # execute sql statement with above statement as arg

            self.mycursor.execute('UPDATE employees SET Name=%s, Department=%s, Title=%s, Pay_Rate=%s, Phone_Number=%s, Work_Type=%s WHERE ID=%s',
                    (f'{name}', f'{dept}', f'{title}', f'{pay_rate}', f'{phone_number}', f'{work_type}', f'{ID}'))
            self.mydb.commit()

            message = 'The employee has been updated'

        elif ID not in self.__employees:
            message = 'No employee found under this ID'

        messagebox.showinfo(title='Info', message=message)

        self.__clear_gui_entry_fields()

    def __delete_employee(self):
        ''' deletes the employee from the app by locating it by ID in dictionary
        '''

        # get values from entry box widget
        ID = self.id_output_entry.get()

        try:
            self.mycursor.execute('DELETE FROM employees WHERE ID = %s', (ID,))
            self.mydb.commit()
        except mysql.connector.Error as err:
            print('Exception caught: ' + str(err))

        # to delete an employee, must be in db. Perform this check
        if ID in self.__employees:
            del self.__employees[ID]
            message = 'Employee deleted'
        else:
            message = 'The specified ID number was not found'

        messagebox.showinfo(title='Info', message=message)

        self.__clear_gui_entry_fields()

        self.__check_db_size()

    def __reset_system(self):
        ''' actions performed to reset the app - deletes app memory, db, and .dat file
        '''

        if messagebox.askquestion(title='Reset System', message='Are you sure you want to delete everything in your employee database?') == 'yes':
            # function to reset app data, in case company leaves. This will delete all data in app and the whole database
            self.__employees = {}

            try:
                self.mycursor.execute('DROP TABLE employees')

                if(os.path.isfile(SAVED_EMPLOYEES_DATA_FILE) and os.access(SAVED_EMPLOYEES_DATA_FILE, os.W_OK)):
                    os.remove(SAVED_EMPLOYEES_DATA_FILE)

                messagebox.showinfo(title='Info', message='System has been reset: database table and ' + SAVED_EMPLOYEES_DATA_FILE[3:] + ' deleted')
            except mysql.connector.Error as err:
                messagebox.showerror(title='Info', message='Database not found, file not found\n' + str(err))
            except FileNotFoundError as err:
                messagebox.showerror(title='Info', message='.dat data file not found\n' + str(err))

            self.reset_button['state'] = self.delete_emp_button['state'] = self.update_emp_button['state'] = self.look_up_emp_button['state'] = DISABLED

        self.__clear_gui_entry_fields()

    def __load_file(self):
        ''' actions performed for when loading the .dat data file into the app
        '''

        # function to load binary file, data is automatically saved from the last time app is used

        try:
            if os.path.isfile(SAVED_EMPLOYEES_DATA_FILE) and os.access(SAVED_EMPLOYEES_DATA_FILE, os.R_OK) \
                and os.stat(SAVED_EMPLOYEES_DATA_FILE).st_size != 0:
                file_obj = open(SAVED_EMPLOYEES_DATA_FILE, 'rb')
                content = pickle.load(file_obj)

                try:
                    while content != ' ':
                        ID = content.get_id_number()
                        if ID not in self.__employees:
                            self.__employees[ID] = EMS.Employee_Management_System(ID, content.get_name(), content.get_department(),
                                     content.get_title(), content.get_pay_rate(),
                                     content.get_phone_number(), content.get_work_type())

                        content = pickle.load(file_obj)

                    file_obj.close()

                except EOFError as err:
                    content = []

        except FileNotFoundError as err:
            messagebox.showerror(title='Info', message='File not found\n' + str(err))

        self.__clear_gui_entry_fields()

    def __clear_gui_entry_fields(self):
        ''' clears all values in the gui text fields, used after clicking a button
        '''

        # set all entry widgets to a blank value
        self.output_entry_var1.set(''), self.output_entry_var2.set('Enter name...'), self.output_entry_var3.set('Enter dept...'),
        self.output_entry_var4.set('Enter title...'), self.output_entry_var5.set('Enter pay...'),
        self.output_entry_var6.set('XXX-XXX-XXXX'), self.radio_var.set(0), self.id_output_entry.focus_set()

        entry_list = [self.name_output_entry, self.dept_output_entry, self.job_title_output_entry,
                     self.pay_rate_output_entry, self.phone_num_output_entry]

        for entry in entry_list:
            entry.update()
            entry.config(foreground='grey')
            entry.config(validate="key")
            entry.config(validatecommand=(self.main_window.register(self.__validate_entry), '%P'))

    def __on_hover(self, event):
        ''' when user hovers over a button, the button's background color and border width are changed to what is specified below
        '''

        event.widget['bg'] = 'lightgrey'
        event.widget['borderwidth'] = 3.8

    def __on_leave(self, event):
        ''' when user stops hovers over a button, the button's background color and border width are changed to default values
        '''

        event.widget['bg'] = 'SystemButtonFace'
        event.widget['borderwidth'] = 3

    def __on_click(self, event):
        ''' erases the auto inserted GUI startup entry box text
        '''

        # sets the entry box's text to be black and deletes existing text
        event.widget.config(foreground='black')
        event_widget = event.widget.get()

        if event_widget in ['Enter id...', 'Enter name...', 'Enter dept...', 'Enter title...', 'Enter pay...', 'XXX-XXX-XXXX']:
            event.widget.delete(0, tk.END)

    def __focus_out(self, event, entry_widget):

        if entry_widget == self.id_output_entry and self.output_entry_var1.get().strip() == '':
            self.output_entry_var1.set('Enter id...')

        elif entry_widget == self.name_output_entry and self.output_entry_var2.get().strip() == '':
            self.output_entry_var2.set('Enter name...')

        elif entry_widget == self.dept_output_entry and self.output_entry_var3.get().strip() == '':
            self.output_entry_var3.set('Enter dept...')

        elif entry_widget == self.job_title_output_entry and self.output_entry_var4.get().strip() == '':
            self.output_entry_var4.set('Enter title...')

        elif entry_widget == self.pay_rate_output_entry and self.output_entry_var5.get().strip() == '':
            self.output_entry_var5.set('Enter pay...')

        elif entry_widget == self.phone_num_output_entry and self.output_entry_var6.get().strip() == '':
            self.output_entry_var6.set('XXX-XXX-XXXX')

        else:
            return

        entry_widget.update()
        entry_widget.config(foreground='grey')
        entry_widget.config(validate="key")
        entry_widget.config(validatecommand=(self.main_window.register(self.__validate_entry), '%P'))


# start xampp control panel using the subprocess module
try:
    xampp = subprocess.Popen('C:\\xampp\\xampp-control.exe')
except FileNotFoundError:
    print("XAMPP control panel executable file not found")
except PermissionError:
    print("Insufficient permissions to execute XAMPP control panel")

# wait 1/2 a second after launching XAMPP to make sure that Apache and MySQL services
# started if user has auto launch enabled in XAMPP config.
# This is to ensure that later when we attempt to connect to the
# database the service had enough time to start before doing this
time.sleep(0.5)

# defines the file to save the apps employee profiles to. The saved file can be loaded later
SAVED_EMPLOYEES_DATA_FILE = '..\\Employees.dat'

# create instance of EMSGui class
app = EMSGui()

# statement needed to launch gui window
app.main_window.mainloop()
