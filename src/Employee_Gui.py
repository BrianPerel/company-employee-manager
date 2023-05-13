'''
Author @ Brian Perel
GUI Employee Management System using XAMPP and sql-connect module
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
import os

class EMSGui:

    # print(__doc__)
    def __init__(self):

        self.start_db_connection()

        ''' create and place main gui window, buttons, labels, entry's, and a canvas1 line '''
        self.main_window = tk.Tk() # make the GUI window
        self.main_window.geometry('520x420') # width x height of the GUI window
        self.main_window.iconphoto(True, PhotoImage(file='../res/icon.png'))
        self.main_window.configure(background='lightgrey') # app (GUI) background color
        self.main_window.title('EMS') # app title
        self.main_window.resizable(0, 0) # disable resizable option for GUI
        self.main_window.eval('tk::PlaceWindow . center') # launches the GUI in the center of the screen

        # create a GUI label (display EMPLOYEE MANAGEMENT SYSTEM) = the header of the GUI app
        self.header = tk.Label(text='EMPLOYEE MANAGEMENT SYSTEM',
                               font='Times 12 bold', bg='lightgrey')

        # build line between header and body of app
        self.canvas1 = tk.Canvas(self.main_window, width=495, height=40, bd=0,
                            borderwidth=0, bg='lightgrey', highlightthickness=0.5,
                            highlightbackground='lightgrey')

        # create line between header and body of app
        self.canvas1.create_line(2, 25, 800, 25, width=2)

        # GUI button 1
        self.look_up_emp_button = tk.Button(text='Look Up Employee',
                        command=self.look_up_employee, bg='SystemButtonFace')

        # GUI message displayed in window (Label)
        self.label1 = tk.Label(text='\tEmployee ID:', font=('Courier', 10), bg='lightgrey')

        # create StringVar variables to store value input into entry box widget
        self.output_entry_var1 = tk.StringVar()
        self.output_entry_var2 = tk.StringVar()
        self.output_entry_var3 = tk.StringVar()
        self.output_entry_var4 = tk.StringVar()
        self.output_entry_var5 = tk.StringVar()
        self.output_entry_var6 = tk.StringVar()
        self.cb_var1 = tk.StringVar()

        # (self.cb_var1) = store app input value into check box variable
        # value is preselected to be 1 to automatically close the connection

        # create an output box (GUI entry)
        self.id_output_entry = tk.Entry(width=15,
                                textvariable=self.output_entry_var1, font=('Courier', 10), bd=2,
                                highlightthickness=1, highlightcolor='black')

        # sets focus on the first text field in app on startup
        self.id_output_entry.focus_set()

        # GUI button
        self.add_emp_button = tk.Button(text='Add New Employee', command=self.add_employee)

        # create label
        self.label2 = tk.Label(text='\tEmployee Name:', font=('Courier', 10),
                                                               bg='lightgrey')

        # take entry box variable and perform action
        self.name_output_entry = tk.Entry(width=15,
                            textvariable=self.output_entry_var2, font=('Courier', 10), bd=2,
                                highlightthickness=1, highlightcolor='black', foreground='gray')

        self.name_output_entry.insert(0, 'Enter name...')
        self.name_output_entry.bind('<Button-1>', self.on_click)
        self.name_output_entry.bind('<FocusIn>', self.on_click)

        # GUI button (update employee)
        self.update_emp_button = tk.Button(text='Update Employee', command=self.update_employee)

        self.label3 = tk.Label(text='\tEmployee Dept:', font=('Courier', 10),
                                                       bg='lightgrey')

        # take entry box variable and perform action
        self.dept_output_entry = tk.Entry(width=15,
                                textvariable=self.output_entry_var3, font=('Courier', 10), bd=2,
                                highlightthickness=1, highlightcolor='black', foreground='gray')

        self.dept_output_entry.insert(0, 'Enter dept...')
        self.dept_output_entry.bind('<Button-1>', self.on_click)
        self.dept_output_entry.bind('<FocusIn>', self.on_click)

        # GUI buttons (delete employee)
        self.delete_emp_button = tk.Button(text='Delete Employee', command=self.delete_employee)

        # display formatted label
        self.label4 = tk.Label(text='\tEmployee Title:', font=('Courier', 10),
                                                       bg='lightgrey')

        # take entry box variable and perform action
        self.job_title_output_entry = tk.Entry(width=15,
                                textvariable=self.output_entry_var4, font=('Courier', 10), bd=2,
                                highlightthickness=1, highlightcolor='black', foreground='grey')

        self.job_title_output_entry.insert(0, 'Enter title...')
        self.job_title_output_entry.bind('<Button-1>', self.on_click)
        self.job_title_output_entry.bind('<FocusIn>', self.on_click)

        # GUI formatted buttons, call appropriate method when clicked
        self.reset_button = tk.Button(text='Reset System', command=self.reset_system)

        # display formatted label
        self.label5 = tk.Label(text='\tPay Rate:', font=('Courier', 10), bg='lightgrey')

        # take entry box variable and perform action
        self.pay_rate_output_entry = tk.Entry(width=15,
                                textvariable=self.output_entry_var5, font=('Courier', 10), bd=2,
                                highlightthickness=1, highlightcolor='black', foreground='grey')

        self.pay_rate_output_entry.insert(0, 'Enter pay...')
        self.pay_rate_output_entry.bind('<Button-1>', self.on_click)
        self.pay_rate_output_entry.bind('<FocusIn>', self.on_click)

        # Opens xampp's MySQL module's admin website via direct link
        self.visit_db_button = tk.Button(text='Visit DB website',
            command=lambda: webbrowser.open(\
                'http://localhost/phpmyadmin/index.php?route=/sql&server=1&db=employee_db&table=employees&pos=0', new=1))

        # display formatted label
        self.label6 = tk.Label(text='\tPhone Number:', font=('Courier', 10), bg='lightgrey')

        self.phone_num_output_entry = tk.Entry(width=15,
                                textvariable=self.output_entry_var6, font=('Courier', 10), bd=2,
                                highlightthickness=1, highlightcolor='black', foreground='grey')

        self.phone_num_output_entry.insert(0, 'Enter phone#...')
        self.phone_num_output_entry.bind('<Button-1>', self.on_click)
        self.phone_num_output_entry.bind('<FocusIn>', self.on_click)

        # store input value from app into radio button variable
        self.radio_var = tk.IntVar()

        # reset radio button variable to option blank (0)
        self.radio_var.set(0)

        self.load_button = tk.Button(text='Load File', command=self.load_file)

        self.quit_button = tk.Button(text='Quit Program', command=self.close_app)

        # create radio button
        self.rb1 = tk.Radiobutton(text='Part Time Employee', variable=self.radio_var,
                                    bg='lightgrey', value=1, cursor='hand2')

        # create radio button
        self.rb2 = tk.Radiobutton(text='Full Time Employee', variable=self.radio_var,
                                    bg='lightgrey', value=2, cursor='hand2')

        # attempts a select query on db table to check if the database is empty. If it is then start GUI with these 2 buttons disabled
        try:
            self.mycursor.execute('SELECT * FROM employees')
        except mysql.connector.Error:
            self.reset_button['state'] = self.load_button['state'] = self.delete_emp_button['state'] = self.look_up_emp_button['state'] = DISABLED

        buttons = [self.look_up_emp_button, self.add_emp_button, self.update_emp_button, self.delete_emp_button, self.reset_button,
                        self.visit_db_button, self.load_button, self.quit_button]

        for button in buttons:
            button.config(font=('Courier', 10), borderwidth=3, cursor='hand2')
            button.bind('<Enter>', self.on_hover)
            button.bind('<Leave>', self.on_leave)

        # build line between body of app and footer
        self.canvas2 = tk.Canvas(self.main_window, width=495, height=40, bd=0,
                            borderwidth=0, bg='lightgrey', highlightthickness=0.5,
                            highlightbackground='lightgrey')

        # create line between body of app and footer
        self.canvas2.create_line(2, 25, 600, 25, width=2)

        # display formatted label in app
        self.label7 = tk.Label(text='created by Brian Perel', font=('Courier', 10), bg='lightgrey')

        # make program position and display all gui components (widgets)
        self.header.place(x=120, y=2)
        self.canvas1.place(x=10, y=20)
        self.look_up_emp_button.place(x=10, y=65)
        self.label1.place(x=203, y=67)
        self.id_output_entry.place(x=380, y=67)
        self.add_emp_button.place(x=10, y=105)
        self.label2.place(x=186, y=107)
        self.name_output_entry.place(x=380, y=107)
        self.update_emp_button.place(x=10, y=145)
        self.label3.place(x=187, y=147)
        self.dept_output_entry.place(x=380, y=147)
        self.delete_emp_button.place(x=10, y=185)
        self.label4.place(x=180, y=187)
        self.job_title_output_entry.place(x=380, y=187)
        self.label5.place(x=230, y=225)
        self.pay_rate_output_entry.place(x=380, y=227)
        self.label6.place(x=200, y=265)
        self.phone_num_output_entry.place(x=380, y=267)
        self.rb1.place(x=240, y=307)
        self.rb2.place(x=380, y=307)
        self.reset_button.place(x=10, y=225)
        self.visit_db_button.place(x=10, y=265)
        self.load_button.place(x=10, y=305)
        self.quit_button.place(x=110, y=305)
        self.canvas2.place(x=10, y=340)
        self.label7.place(x=160, y=380)

        # create a new file only if file doesn't exist, otherwise don't
        if not os.path.isfile(SAVED_EMPLOYEES_DATA_FILE):
            # create a new binary file to store binary object info, if one doesn't already exist in folder
            file_obj = open(SAVED_EMPLOYEES_DATA_FILE, 'wb')
            file_obj.close()

        # listens for when 'x' exit button is pressed and routes to close_app
        self.main_window.protocol('WM_DELETE_WINDOW', self.close_app)

        # statement needed to launch gui window
        self.main_window.mainloop()

    # App operations:

    # create the empty dictionary
    employees = {}

    def start_db_connection(self):
        ''' actions to create and start the db connection
        '''

        # connect to the database using credentials
        try:
            # host='localhost', port=3306
            self.mydb = mysql.connector.connect(
            host='localhost', port=3306, user='root')

        except mysql.connector.Error as err:
            print('Exception caught: ' + str(err))

        # create the empty database and table, if needed (first run)
        self.mycursor = self.mydb.cursor(buffered=True)
        self.mycursor.execute('CREATE DATABASE IF NOT EXISTS employee_db')
        self.mycursor.execute('use employee_db')

    def close_app(self):
        ''' performs actions when closing the app
        '''

        # Value 1 stands for checked check box, if user puts checkmark, we close the db connection to localhost
        if self.cb_var1.get() == 1:
            self.mydb.close()

        # close xampp app
        xampp.terminate()

        # close gui window
        self.main_window.destroy()

    def look_up_employee(self):
        ''' actions performed for when looking up an employee
        '''

        # create the empty database and table
        self.mycursor = self.mydb.cursor(buffered=True)

        # function to look up an employee's info in dictionary, by the ID attained from GUI
        # Get an employee ID number to look up.
        ID = self.id_output_entry.get()

        # ternary operator
        message = self.employees.get(ID) if (ID in self.employees) else 'No employee found under this ID'

        # create a showinfo message box
        messagebox.showinfo(title='Employee Info', message=str(message))

        self.clear_gui_entry_fields()

    def add_employee(self, check=True, work_type=''):
        ''' actions for when adding an employee, add an employee to dictionary, by info gathered from GUI
        '''

        self.mycursor = self.mydb.cursor(buffered=True)
        self.mycursor.execute('CREATE TABLE IF NOT EXISTS employees (Employee_Creation_Date VARCHAR(30), ID INT PRIMARY KEY, \
                            Name VARCHAR(30), Department VARCHAR(30), \
                            Title VARCHAR(30), Pay_Rate VARCHAR(30), \
                            Phone_Number VARCHAR(30), \
                            Work_Type VARCHAR(30))')

        try:
            date = str(datetime.now().strftime("%m-%d-%Y %I:%M %p"))
            ID = self.id_output_entry.get()
            name = self.name_output_entry.get().title().strip()
            dept = self.dept_output_entry.get().title().strip()
            title = self.job_title_output_entry.get().title().strip()
            pay_rate = self.pay_rate_output_entry.get().strip()
            phone_number = self.phone_num_output_entry.get().strip()

        except ValueError as err:
            print('Exception caught: ' + str(err))
            check = False

        if name == 'Enter name...' or dept == 'Enter dept...' or title == 'Enter title...' \
        or pay_rate == 'Enter pay...' or phone_number == 'Enter phone#...':
            messagebox.showerror(title='Info', message='Could not add employee.')
            self.clear_gui_entry_fields()
            return

        # if user entered phone number without including dashes, manually attach them
        if '(' or ')' not in phone_number:
            phone_number = '(' + phone_number[:3] + ')' + phone_number[3:]

        if '-' not in phone_number:
            phone_number = phone_number[:5] + '-' + phone_number[5:8] + '-' + phone_number[8:]

        # use regular expressions to check format of info given
        # name, dept, title should all only contain letters, if nums are contained then mark
        pattern1 = bool(regular_exp.match('[a-zA-Z]+', name))
        name_has_digit = any(item.isdigit() for item in name)

        pattern2 = bool(regular_exp.match('[a-zA-Z]+', dept))
        dept_has_digit = any(item.isdigit() for item in dept)

        pattern3 = bool(regular_exp.match('[a-zA-Z]+', title))
        title_has_digit = any(item.isdigit() for item in title)

        # value of 1 stands for part time radio button option, 2 for full time option
        if self.radio_var.get() == 1:
            work_type = 'Part time'
        elif self.radio_var.get() == 2:
            work_type = 'Full time'

        # if user provides a pay rate
        if(len(pay_rate) == 0):
            # show info message box with data
            messagebox.showerror(title='Info', message='Could not add employee.')
            self.clear_gui_entry_fields()
            return

        # if user entered $ in pay_rate, remove it to enable casting to float which we do to format the number
        if('$' in pay_rate):
            pay_rate = pay_rate.replace('$', '')

        pay_rate_has_letters = any(item.isalpha() for item in pay_rate)

        # cast to float and format number, cast pay_rate back to string
        if not pay_rate_has_letters:
            pay_rate = str(format(float(pay_rate), '.2f'))
        else:
            messagebox.showerror(title='Info', message='Could not add employee.')
            self.clear_gui_entry_fields()
            return

        # create instance and send the values
        new_emp = EMS.Employee(ID, name, dept, title, pay_rate, phone_number, work_type)

        # conditional statement to add employee into dictionary
        if ID not in self.employees and len(phone_number) == 14 and check and len(ID) == 6 \
           and '' not in [name, dept, title, pay_rate, phone_number, work_type] \
           and pattern1 and pattern2 and pattern3 and not name_has_digit \
           and not dept_has_digit and not title_has_digit:
            self.employees[ID] = new_emp
            message = 'The new employee has been added'

            # if db exists (at least 1 record has been added to db table) then enable the look up and reset buttons
            if self.reset_button['state'] == DISABLED or self.look_up_emp_button['state'] == DISABLED:
                self.reset_button['state'] = self.load_button['state'] = self.delete_emp_button['state'] = self.look_up_emp_button['state'] = NORMAL

            # add a $ to pay_rate before adding it to the table in database
            pay_rate = pay_rate[:pay_rate.find(pay_rate)] + '$' + pay_rate[pay_rate.find(pay_rate):]

            # serialize the object
            file_obj = open(SAVED_EMPLOYEES_DATA_FILE, 'ab')
            pickle.dump(new_emp, file_obj)
            file_obj.close()

            # insert data into db table
            try:
                self.mycursor.execute('INSERT INTO employees (Employee_Creation_Date, ID, Name, Department, Title, \
            Pay_Rate, Phone_Number, Work_Type) values (%s, %s, %s, %s, %s, %s, %s, %s)',
            (date, ID, name, dept, title, pay_rate, phone_number, work_type))
                self.mydb.commit()
            except mysql.connector.Error as err:
                message = 'An employee with that ID already exists.'
                self.clear_gui_entry_fields()
                print('Exception caught: ' + str(err))

        # input validation: make sure no fields are blank and input of proper lengths is given
        elif '' in [ID, name, dept, title, pay_rate, phone_number, work_type] \
             or not check or len(ID) != 6 or not pattern1 \
             or not pattern2 or not pattern3 or name_has_digit \
             or dept_has_digit or title_has_digit or len(phone_number) != 14:
            message = 'Could not add employee.'
        elif ID in self.employees:
            message = 'An employee with that ID already exists.'

        # show info message box with data
        messagebox.showinfo(title='Info', message=message)

        self.clear_gui_entry_fields()

    def update_employee(self, check=True, message=''):
        ''' actions performed to update an employee's data in the app by attaining info from GUI and
            updating an already existing employee's info in the dictionary
        '''

        # create the empty database and table
        self.mycursor = self.mydb.cursor(buffered=True)
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

        if ID in self.employees:
            name, dept = self.name_output_entry.get(), self.dept_output_entry.get()
            title, pay_rate = self.job_title_output_entry.get(), self.pay_rate_output_entry.get()
            phone_number = self.phone_num_output_entry.get()

            # create radio buttons: 0 is none selected, 1 is first circle, 2 is second
            if self.radio_var.get() == 0:
                messagebox.showinfo(title='Info', message='Couldn\'t update employees info')
            elif self.radio_var.get() == 1:
                work_type = 'Part time'
            elif self.radio_var.get() == 2:
                work_type = 'Full time'

            # store employee object in employee dictionary, the dictionary's key is the employee's ID
            self.employees[ID] = EMS.Employee(ID, name, dept,
                                    title, pay_rate, phone_number, work_type)

            check = 'SELECT * FROM employees WHERE ID = %s'
            self.mycursor.execute(check, (ID,))  # execute sql statement with above statement as arg

            self.mycursor.execute('UPDATE employees SET Name=%s, Department=%s, Title=%s, Pay_Rate=%s, Phone_Number=%s, Work_Type=%s WHERE ID=%s',
                    (f'{name}', f'{dept}', f'{title}', f'{pay_rate}', f'{phone_number}', f'{work_type}', f'{ID}'))
            self.mydb.commit()

            message = 'The new employee has been updated'

        elif not check:
            message = 'Couldn\'t update employees info.'
        elif ID not in self.employees:
            message = 'No employee found under this ID'

        messagebox.showinfo(title='Info', message=message)

        self.clear_gui_entry_fields()

    def delete_employee(self):
        ''' deletes the employee from the app by locating it by ID in dictionary
        '''

        # create the empty database and table
        self.mycursor = self.mydb.cursor(buffered=True)

        # get values from entry box widget
        ID = self.id_output_entry.get()

        try:
            self.mycursor.execute('DELETE FROM employees WHERE ID = %s', (ID,))
            self.mydb.commit()

        except mysql.connector.Error as err:
            print('Exception caught: ' + str(err))

        # to delete an employee, must be in db. Perform this check
        if ID in self.employees:
            del self.employees[ID]
            message = 'Employee deleted'
        else:
            message = 'The specified ID number was not found'

        messagebox.showinfo(title='Info', message=message)

        self.clear_gui_entry_fields()

    def reset_system(self):
        ''' actions performed to reset the app - deletes app memory, db, and .dat file
        '''

        if messagebox.askquestion(title='Reset System' , message='Are you sure you want to delete everything in your employee database?') == 'yes':
            self.mycursor = self.mydb.cursor(buffered=True)

            # function to reset app data, in case company leaves. This will delete all data in app and the whole database
            self.employees = {}

            try:
                self.mycursor.execute('DROP TABLE employees')
                os.remove(SAVED_EMPLOYEES_DATA_FILE)
                messagebox.showinfo(title='Info', message='System has been reset: database table and ' + SAVED_EMPLOYEES_DATA_FILE[3:] + ' deleted')
            except mysql.connector.Error as err:
                messagebox.showerror(title='Info', message='Database not found, file not found\n' + str(err))
            except FileNotFoundError as err:
                messagebox.showerror(title='Info', message='File not found\n' + str(err))

            self.reset_button['state'] = self.load_button['state'] = self.delete_emp_button['state'] = self.look_up_emp_button['state'] = DISABLED

        self.clear_gui_entry_fields()

    def load_file(self):
        ''' actions performed for when loading the .dat data file into the app
        '''

        # function to load binary file, data is automatically saved from the last time app is used

        try:
            if not os.path.isfile(SAVED_EMPLOYEES_DATA_FILE):
                messagebox.showinfo(title='Info', message='Cannot load directories')
            elif not os.access(SAVED_EMPLOYEES_DATA_FILE, os.R_OK):
                messagebox.showinfo(title='Info', message='Cannot read file')
            elif os.stat(SAVED_EMPLOYEES_DATA_FILE).st_size == 0:
                messagebox.showinfo(title='Info', message='File is empty')

            else:
                file_obj = open(SAVED_EMPLOYEES_DATA_FILE, 'rb')
                content = pickle.load(file_obj)

                try:
                    while content != ' ':
                        messagebox.showinfo(title='Info', message=content)
                        #                        messagebox.showinfo(title = 'Info', message = 'Data loaded from ' + SAVED_EMPLOYEES_DATA_FILE + ' saved data file:\n\n' + content)

                        ID = content.get_id_number()
                        if ID not in self.employees:
                            self.employees[ID] = EMS.Employee(ID, content.get_name(), content.get_department(),
                                     content.get_title(), content.get_pay_rate(),
                                     content.get_phone_number(), content.get_work_type())

                        content = pickle.load(file_obj)

                    file_obj.close()

                except EOFError as err:
                    content = []

        except FileNotFoundError as err:
            messagebox.showerror(title='Info', message='File not found\n' + str(err))

        self.clear_gui_entry_fields()

    def clear_gui_entry_fields(self):
        ''' clears all values in the gui text fields, used after clicking a button
        '''

        self.name_output_entry.config(foreground='grey'), self.dept_output_entry.config(foreground='grey'),
        self.job_title_output_entry.config(foreground='grey'), self.pay_rate_output_entry.config(foreground='grey'),
        self.phone_num_output_entry.config(foreground='grey')

        # set all entry widgets to a blank value
        self.output_entry_var1.set(''), self.output_entry_var2.set('Enter name...'), self.output_entry_var3.set('Enter dept...'),
        self.output_entry_var4.set('Enter title...'), self.output_entry_var5.set('Enter pay...'),
        self.output_entry_var6.set('Enter phone#...'), self.radio_var.set(0), self.id_output_entry.focus_set()

    def on_hover(self, e):
        ''' when user hovers over a button, the button's background color and border width are changed to what is specified below
        '''

        e.widget['bg'] = 'lightgrey'
        e.widget['borderwidth'] = 3.8

    def on_leave(self, e):
        ''' when user stops hovers over a button, the button's background color and border width are changed to default values
        '''

        e.widget['bg'] = 'SystemButtonFace'
        e.widget['borderwidth'] = 3

    def on_click(self, event):
        ''' erases the auto inserted GUI startup entry box text
        '''

        # sets the entry box's text to be black and deletes existing text
        event.widget.config(foreground='black')
        event_widget = event.widget.get()

        if event_widget in ['Enter name...', 'Enter dept...', 'Enter title...', 'Enter pay...', 'Enter phone#...']:
            event.widget.delete(0, tk.END)


# start_db_connection xampp using the subprocess module
xampp = subprocess.Popen('C:\\xampp\\xampp-control.exe')

# defines the file to save the apps employee profiles to. The saved file can be loaded later
SAVED_EMPLOYEES_DATA_FILE = '..\\Employees.dat'

# create instance of EMSGui class
EMSGui()
