'''
Author @ Brian Perel
GUI Employee Management System using XAMPP and sql-connect module
-> Python UI program that will store information about employees in a company using a dictionary with remove, update, loop up operations
-> Uses an employee class to set and get employee attributes

-> Programs requires user to start XAMPP, Apache server and MySQL module 
'''

import tkinter as tk 
import tkinter.messagebox as messagebox
import Employee_Management_System as EMS
import mysql.connector
import subprocess
import pickle
import re, os

class MyGUI: 
    
    def __init__(self):
        ''' create and place main gui window, buttons, labels, entry's, and a canvas line '''
        self.main_window = tk.Tk() # make the GUI window
        self.main_window.geometry('520x390') # width x height
        self.main_window.configure(background='lightgrey') # app background color 
        self.main_window.title('Company') # app title
        self.main_window.resizable(0, 0)

        # start xampp app -- the following commented out code was blocked because of a taskkill issue
        # instead I'm using subprocess module to open and close xampp 
         
        #try:
        #   os.startfile('C:\\xampp\\xampp-control.exe')

        #except Exception as e:
        #   print(str(e))

        # create a GUI label (display EMPLOYEE MANAGEMENT SYSTEM) = the header of the GUI app
        self.header = tk.Label(text = 'EMPLOYEE MANAGEMENT SYSTEM',
                               font = 'Times 12 bold', bg='lightgrey')

        # build line between header and body of app 
        self.canvas = tk.Canvas(self.main_window, width=495, height=40, bd=0, \
                            borderwidth=0, bg='lightgrey', highlightthickness=0.5, \
                            highlightbackground='lightgrey')

        # create line between header and body of app 
        self.canvas.create_line(2, 25, 800, 25)
                
        # GUI button 1
        self.my_button1 = tk.Button(text = 'Look Up Employee', \
                        command = self.look_up_employee, font = 'Courier 10')

        # GUI message displayed in window (Label)
        self.label1 = tk.Label(text = '\tEmployee ID:', font = 'Courier 10', \
                                                               bg='lightgrey')

        # create a StringVar variable to store value input into entry box widget 
        self.output_entry_var = tk.StringVar()

        # create an output box (GUI entry)
        self.output_entry = tk.Entry(width = 20, \
                                textvariable = self.output_entry_var) 
        
        # sets focus on the first text field in app on startup
        self.output_entry.focus_set()
        
        # GUI button
        self.my_button2 = tk.Button(text = 'Add New Employee',
                            font = 'Courier 10', \
                            command = self.add_employee)

        # create label 
        self.label2 = tk.Label(text = '\tEmployee Name:', font = 'Courier 10', \
                                                               bg='lightgrey')

        # create a StringVar variable to store value input into entry box widget 
        self.output_entry_var1 = tk.StringVar()

        # take entry box variable and perform action  
        self.output_entry1 = tk.Entry(width = 20, \
                            textvariable = self.output_entry_var1)

        # GUI button (update employee)
        self.my_button3 = tk.Button(text = 'Update Employee', \
                                    font = 'Courier 10', \
                                    command = self.update_employee)

        self.label3 = tk.Label(text = '\tEmployee Dept:', font = 'Courier 10', \
                                                       bg='lightgrey')
        
        # create a StringVar variable to store value input into entry box widget 
        self.output_entry_var2 = tk.StringVar()
        
        # take entry box variable and perform action  
        self.output_entry2 = tk.Entry(width = 20, \
                                textvariable = self.output_entry_var2)

        # GUI buttons (delete employee) 
        self.my_button4 = tk.Button(text = 'Delete Employee', \
                                        font = 'Courier 10', \
                                        command = self.delete_employee)

        # display formatted label 
        self.label4 = tk.Label(text = '\tEmployee Title:', font = 'Courier 10', \
                                                       bg='lightgrey')

        # create a StringVar variable to store value input into entry box widget 
        self.output_entry_var3 = tk.StringVar()

        # take entry box variable and perform action  
        self.output_entry3 = tk.Entry(width = 20, \
                                    textvariable = self.output_entry_var3)

        # display formatted label 
        self.label5 = tk.Label(text = '\tPay Rate:', font = 'Courier 10', \
                                                        bg='lightgrey')

        # create a StringVar variable to store value input into entry box widget 
        self.output_entry_var4 = tk.StringVar()

        # take entry box variable and perform action  
        self.output_entry4 = tk.Entry(width = 20, \
                                    textvariable = self.output_entry_var4)

        # display formatted label 
        self.label6 = tk.Label(text = '\tPhone Number:', font = 'Courier 10', \
                                                        bg='lightgrey')

        self.output_entry_var5 = tk.StringVar()

        self.output_entry5 = tk.Entry(width = 20, \
                                    textvariable = self.output_entry_var5)

        # store input value from app into radio button variable 
        self.radio_var = tk.IntVar()
        # reset radio button variable to option blank (0) 
        self.radio_var.set(0)

        # create radio button
        self.rb1 = tk.Radiobutton(text='Part Time Employee', variable=self.radio_var, \
                                    bg='lightgrey', value=1)

        # create radio button 
        self.rb2 = tk.Radiobutton(text='Full Time Employee', variable=self.radio_var, \
                                    bg='lightgrey', value=2)

        #GUI formatted buttons, call appropriate method when clicked 
        self.reset_button = tk.Button(text='Reset System', font = 'Courier 10', \
                                           command = self.reset_system)

        
        self.quit_button = tk.Button(text='Quit Program', font = 'Courier 10',
        command = self.close_app)

        self.load_button = tk.Button(text='Load File', font = 'Courier 10', command = self.load_file)

        # build line between body of app and footer 
        self.canvas2 = tk.Canvas(self.main_window, width=495, height=40, bd=0, \
                            borderwidth=0, bg='lightgrey', highlightthickness=0.5, \
                            highlightbackground='lightgrey')

        # create line between body of app and footer 
        self.canvas2.create_line(2, 25, 800, 25)


        # display formatted label in app 
        self.label7 = tk.Label(text = 'created by Brian Perel', font = 'Courier 10', \
                                                        bg='lightgrey')

        # store app input value into check box variable 
        self.cb_var1 = tk.IntVar()

        self.conn_close = tk.Checkbutton(text='Close MySQL Connection', variable = self.cb_var1, bg='lightgrey')

        # Value 1 stands for checked check box, if user puts checkmark, we close the db connection to localhost 
        if self.cb_var1.get() == 1:
            self.mydb.close()

        # make program position and display all gui components (widgets) 
        self.header.place(x = 120, y = 0)
        self.canvas.place(x = 10, y = 20)
        self.my_button1.place(x = 10, y = 65)
        self.label1.place(x = 203, y = 67)
        self.output_entry.place(x = 380, y = 67)        
        self.my_button2.place(x = 10, y = 105)
        self.label2.place(x = 186, y = 107)
        self.output_entry1.place(x = 380, y = 107)
        self.my_button3.place(x = 10, y = 145)
        self.label3.place(x = 187, y = 147)
        self.output_entry2.place(x = 380, y = 147)
        self.my_button4.place(x = 10, y = 185)
        self.label4.place(x = 180, y = 187)
        self.output_entry3.place(x = 380, y = 187)
        self.label5.place(x = 230, y = 225)
        self.output_entry4.place(x = 380, y = 227)
        self.label6.place(x = 200, y = 265)
        self.output_entry5.place(x = 380, y = 267)
        self.rb1.place(x = 240, y = 305)
        self.rb2.place(x = 380, y = 305)
        self.reset_button.place(x = 10, y = 225)
        self.quit_button.place(x = 110, y = 300)
        self.load_button.place(x = 10, y = 300)
        self.conn_close.place(x = 10, y = 265)
        self.canvas2.place(x = 10, y = 328)
        self.label7.place(x = 160, y = 360)

        # create a new file only if file doesn't exist, otherwise don't
        if not os.path.isfile(DATA_FILE):
            # create a new binary file to store binary object info, if one doesn't
            # already exist in folder 
            file_obj = open(DATA_FILE, 'wb')
            file_obj.close()

        # statement needed to launch gui window 
        self.main_window.mainloop()


# App operations:

    
    # create the empty dictionary
    employees = {}

    # performs actions when closing the app
    def close_app(self):

        # close xampp app 
        xampp.terminate()
        
        # below line is commented because taskkill isn't being recognized
        # os.system('taskkill /im xampp-control.exe')

        # close gui window            
        self.main_window.destroy()

    # actions performed for when looking up an employee
    def look_up_employee(self):

        # connect to the database using credentials 
        try:
            self.mydb = mysql.connector.connect(
                host='localhost', user='root', passwd='', database='employee_db')

        # if can't connect to db then db doesn't exist. Just connect to localhost site 
        except mysql.connector.Error as err:
            self.mydb = mysql.connector.connect(
                host='localhost', user='root', passwd='')

    
        # create the empty databaase and table 
        self.mycursor = self.mydb.cursor(buffered=True)
    
        ''' function to look up an employee's info in dictionary,
        by the ID attained from GUI '''
        # Get an employee ID number to look up.
        ID = self.output_entry.get()

        # ternary operator 
        message = self.employees.get(ID) if (ID in self.employees) else 'No employee found of this ID'

        # create a showinfo message box 
        tk.messagebox.showinfo('Employee Info', str(message))

        # set all entry widgets to a blank value
        self.output_entry_var.set(''), self.output_entry_var1.set('')
        self.output_entry_var2.set(''), self.output_entry_var3.set('')
        self.output_entry_var4.set(''), self.output_entry_var5.set('')
        self.radio_var.set(0)

        try:
            sql = "SELECT * FROM employees WHERE ID = %s"
            self.mycursor.execute(sql, (ID,))
            display_data = self.mycursor.fetchall()
            for data in display_data:
                print("Displaying current employee ID's record: " + data)

        except mysql.connector.Error as err:
            print('Exception caught: ' + err)
            
    # actions for when adding an employee 
    def add_employee(self):

        # connect to the database using credentials 
        try:
            self.mydb = mysql.connector.connect(
                host='localhost', user='root', passwd='', database='employee_db')

        except mysql.connector.Error as err:
            print('Exception caught: ' + err)
            self.mydb = mysql.connector.connect(
                host='localhost', user='root', passwd='')

        # create the empty databaase and table 
        self.mycursor = self.mydb.cursor(buffered=True)
        self.mycursor.execute('CREATE DATABASE IF NOT EXISTS employee_db')
        self.mycursor.execute('use employee_db')
        self.mycursor.execute('CREATE TABLE IF NOT EXISTS employees (ID INT, \
                            Name VARCHAR(30), Deptartment VARCHAR(30),\
                            Title VARCHAR(30), Pay_Rate VARCHAR(30), \
                            Phone_Number VARCHAR(30), \
                            Work_Type VARCHAR(30))')
        
        ''' function to add an employee to dictionary, by info gathered from GUI '''
        # get values from entry box widget
        check = True
        work_type = ''

        # get all data from gui and assign to dictionary values 
        try:
            ID = self.output_entry.get()
            name = self.output_entry1.get()
            dept = self.output_entry2.get()
            title = self.output_entry3.get()
            pay_rate = self.output_entry4.get()
            phone_number = self.output_entry5.get()

            # perform cast operations, since ID should be only INT (whole) value and pay_rate only float (decimal) 
            int(ID)             
            
        except ValueError:
            check = False

        # if user entered phone number without including dashes, manually attach them 
        if "-" not in phone_number:
            p1 = phone_number[:3]
            p2 = phone_number[3:6]
            p3 = phone_number[6:10]
            phone_number = p1 + '-' + p2 + '-' + p3

        # use regular expressions to check format of info given
        # name, dept, title should all only contain letters, if nums are contained then mark 
        pattern1 = bool(re.match('[a-zA-Z]+', name))
        name_hasdigit = any(item.isdigit() for item in name)
        
        pattern2 = bool(re.match('[a-zA-Z]+', dept))
        dept_hasdigit = any(item.isdigit() for item in dept)
        
        pattern3 = bool(re.match('[a-zA-Z]+', title))
        title_hasdigit = any(item.isdigit() for item in title)

        # value of 1 stands for part time radio button option, 2 for full time option 
        if self.radio_var.get() == 1:
            work_type = 'Part time'
        elif self.radio_var.get() == 2:
            work_type = 'Full time'

        # if user provides a pay rate 
        if(len(pay_rate) == 0):
            message = 'Could not add employee.'
            
            # show info message box with data 
            tk.messagebox.showinfo('Info', message)
            return

        # if user entered $ in pay_rate, remove it to enable casting to float which we do to format the number 
        if("$" in pay_rate):
           pay_rate = pay_rate.replace("$", "")

        # cast to float and format number, cast pay_rate back to string 
        pay_rate = str(format(float(pay_rate), '.2f'))

        # create instance and send the values 
        new_emp = EMS.Employee(
                    name, ID, dept, title, pay_rate, phone_number, work_type)

        self.mycursor.execute('CREATE TABLE IF NOT EXISTS employees (ID INT, \
                            Name VARCHAR(30), Deptartment VARCHAR(30), \
                            Title VARCHAR(30), Pay_Rate VARCHAR(30), \
                            Phone_Number VARCHAR(30), Work_Type VARCHAR(30))')

        # conditional statement to add employee into dictionary
        if ID not in self.employees and len(phone_number) == 12 and check == True and len(ID) == 6 and name != '' \
           and dept != '' and title != '' and pay_rate != '' \
           and phone_number != '' and work_type != '' and pattern1 == True \
           and pattern2 == True and pattern3 == True and name_hasdigit == False \
           and dept_hasdigit == False and title_hasdigit == False:
            self.employees[ID] = new_emp
            message = 'The new employee has been added'

            # add a $ to pay_rate before adding it to the table in database 
            index = pay_rate.find(pay_rate)
            pay_rate = pay_rate[:index] + '$' + pay_rate[index:]

            # serialize the object 
            file_obj = open(DATA_FILE, 'ab')
            pickle.dump(new_emp, file_obj)
            
            file_obj.close()

            # insert data into db table 
            sql = 'INSERT INTO employees (ID, Name, Deptartment, Title, \
            Pay_Rate, Phone_Number, Work_Type) values (%s, %s, %s, %s, %s, %s, %s)'
                
            val = (ID, name, dept, title, pay_rate, phone_number, work_type)
            self.mycursor.execute(sql, val)
            self.mydb.commit()

        
        # input validation: make sure no fields are blank  
        elif ID == '' or name == '' or dept == '' or title == '' \
             or pay_rate == '' or phone_number == '' or work_type == '' \
             or check == False or len(ID) < 6 or len(ID) > 6 or pattern1 == False \
             or pattern2 == False or pattern3 == False or name_hasdigit == True \
             or dept_hasdigit == True or title_hasdigit == True or len(phone_number) != 12:
            message = 'Could not add employee.'
        elif ID in self.employees:
            message = 'An employee with that ID already exists.'

        # show info message box with data 
        tk.messagebox.showinfo('Info', message)
        
        # set all entry widgets to a blank value
        self.output_entry_var.set(''), self.output_entry_var1.set('')
        self.output_entry_var2.set(''), self.output_entry_var3.set('')
        self.output_entry_var4.set(''), self.output_entry_var5.set('')
        self.radio_var.set(0)

    # actions performed to updated an employee's data in the app
    def update_employee(self):

        # connect to the database using credentials 
        try:
            self.mydb = mysql.connector.connect(
                host='localhost', user='root', passwd='', database='employee_db')

        # if db doesn't exist then just connect/login into localhost site 
        except mysql.connector.Error as err:
            self.mydb = mysql.connector.connect(
                host='localhost', user='root', passwd='')

        # create the empty databaase and table 
        self.mycursor = self.mydb.cursor(buffered=True)
        self.mycursor.execute('CREATE DATABASE IF NOT EXISTS employee_db')
        self.mycursor.execute('use employee_db')
        self.mycursor.execute('CREATE TABLE IF NOT EXISTS employees (ID INT, \
                            Name VARCHAR(30), Deptartment VARCHAR(30),\
                            Title VARCHAR(30), Pay_Rate VARCHAR(30), \
                            Phone_Number VARCHAR(30), \
                            Work_Type VARCHAR(30))')
        
        ''' function to update an already existing employee's info
            in dictionary, by attaining info from GUI '''
        message = ''
        check = True 
        # get values from entry box widget
        try:
            ID = self.output_entry.get()
            int(ID)

        except ValueError as err:
            print(err)
            check = False

        if ID in self.employees:
            name, dept = self.output_entry1.get(), self.output_entry2.get()
            title, pay_rate = self.output_entry3.get(), self.output_entry4.get()
            phone_number = self.output_entry5.get()

            # create radio buttons: 0 is none selected, 1 is first circle, 2 is second 
            if self.radio_var.get() == 0:
                tk.messagebox.showinfo('Info', 'Couldn\'t update employees info')
            elif self.radio_var.get() == 1:
                work_type = 'Part time'
            elif self.radio_var.get() == 2:
                work_type = 'Full time'

            new_emp = EMS.Employee(name, ID, dept, \
                                    title, pay_rate, phone_number, work_type)

            # store employee object in employee dictionary, the dictionary's key is the employee's ID 
            self.employees[ID] = new_emp

            check = 'SELECT * FROM employees WHERE ID = %s'
            self.mycursor.execute(check, (ID,)) # execute sql statement with above statement as arg 
                
            sql = 'UPDATE employees SET Name=%s, Deptartment=%s, Title=%s, Pay_Rate=%s, Phone_Number=%s, Work_Type=%s WHERE ID=%s'
            val = (f'{name}', f'{dept}', f'{title}', f'{pay_rate}', f'{phone_number}', f'{work_type}', f'{ID}')
            self.mycursor.execute(sql, val)
            self.mydb.commit()
            
            message = 'The new employee has been updated'

        elif check == False:
            message = 'Couldn\'t update employees info.'
        elif ID not in self.employees:
            message = 'No employee found of this ID'

        tk.messagebox.showinfo('Info', message)

        # set all entry widgets to a blank value
        self.output_entry_var.set(''), self.output_entry_var1.set('')
        self.output_entry_var2.set(''), self.output_entry_var3.set('')
        self.output_entry_var4.set(''), self.output_entry_var5.set('')
        self.radio_var.set(0)

    # deletes the employee from the app
    def delete_employee(self):

        # connect to the database using credentials 
        try:
            self.mydb = mysql.connector.connect(
                host='localhost', user='root', passwd='', database='employee_db')

        except mysql.connector.Error as err:
            print('Exception caught: ' + err)
            self.mydb = mysql.connector.connect(
                host='localhost', user='root', passwd='')

        # create the empty databaase and table 
        self.mycursor = self.mydb.cursor(buffered=True)
        
        ''' function to delete an employee from app, by locating it
            by ID in dictionary '''
        # get values from entry box widget 
        ID = self.output_entry.get()

        try:       
            sql = "DELETE FROM employees WHERE ID = %s"
            self.mycursor.execute(sql, (ID,))
            self.mydb.commit()

        except mysql.connector.Error as err:
            print(err)

        # to delete an employee, must be in db. Perform this check 
        if ID in self.employees:
            del self.employees[ID]
            message = 'Employee information deleted'
        else:
            message = 'The specified ID number was not found'

        tk.messagebox.showinfo('Info', message)
        
        # set all entry widgets to a blank value
        self.output_entry_var.set(''), self.output_entry_var1.set('')
        self.output_entry_var2.set(''), self.output_entry_var3.set('')
        self.output_entry_var4.set(''), self.output_entry_var5.set('')
        self.radio_var.set(0)

    # actions performed to reset the app 
    def reset_system(self):

        # connect to the database using credentials 
        try:
            self.mydb = mysql.connector.connect(
                host='localhost', user='root', passwd='', database='employee_db')

        except mysql.connector.Error as err:
            self.mydb = mysql.connector.connect(
                host='localhost', user='root', passwd='')

        # create the empty databaase and table 
        self.mycursor = self.mydb.cursor(buffered=True)
        self.mycursor.execute('CREATE DATABASE IF NOT EXISTS employee_db')
        self.mycursor.execute('use employee_db')
        self.mycursor.execute('CREATE TABLE IF NOT EXISTS employees (ID INT, \
                            Name VARCHAR(30), Deptartment VARCHAR(30),\
                            Title VARCHAR(30), Pay_Rate VARCHAR(30), \
                            Phone_Number VARCHAR(30), \
                            Work_Type VARCHAR(30))')
        
        ''' function to reset app data, in case company leaves.
            This will delete all data in app and database ''' 
        self.employees = {}            

        try:
            self.mycursor.execute('DROP TABLE employees')
            os.remove(DATA_FILE)
            tk.messagebox.showinfo('Info', 'System has been reset, table and ' + DATA_FILE + ' deleted')
        except mysql.connector.Error as err:
            tk.messagebox.showinfo('Info', 'Database not found, file not found\n' + err)
        except FileNotFoundError as err:
            tk.messagebox.showinfo('Info', 'File not found' + err)

        # set all entry widgets to a blank value        
        self.output_entry_var.set(''), self.output_entry_var1.set('')
        self.output_entry_var2.set(''), self.output_entry_var3.set('')
        self.output_entry_var4.set(''), self.output_entry_var5.set('')
        self.radio_var.set(0)

    # actions performed for when loading the .dat data file into the app
    def load_file(self):
        
        # connect to the database using credentials 
        try:
            self.mydb = mysql.connector.connect(
                host='localhost', user='root', passwd='', database='employee_db')

        except mysql.connector.Error as err:
            print('Exception caught: ', err)
            self.mydb = mysql.connector.connect(
                host='localhost', user='root', passwd='')

        # create the empty databaase and table 
        self.mycursor = self.mydb.cursor(buffered=True)
        self.mycursor.execute('CREATE DATABASE IF NOT EXISTS employee_db')
        self.mycursor.execute('use employee_db')
        self.mycursor.execute('CREATE TABLE IF NOT EXISTS employees (ID INT, \
                            Name VARCHAR(30), Deptartment VARCHAR(30),\
                            Title VARCHAR(30), Pay_Rate VARCHAR(30), \
                            Phone_Number VARCHAR(30), \
                            Work_Type VARCHAR(30))')
        
        
        ''' function to load binary file, data is automatically
        saved from the last time app is used '''
        
        try:
            if os.stat(DATA_FILE).st_size == 0:
                message = 'File is empty'
                tk.messagebox.showinfo('Info', message)

            else: 
                file_obj = open(DATA_FILE, 'rb')
                content = pickle.load(file_obj)

                try:
                    while content != ' ':
                        tk.messagebox.showinfo('Info', content)
                        content = pickle.load(file_obj)
                        
                    file_obj.close()
                    
                except EOFError as err:
                    print('Exception caught: ' + err)
            
        except FileNotFoundError as err:
            tk.messagebox.showinfo('Info', 'File not found\n' + err)
  
        
# start xampp app 
xampp = subprocess.Popen('C:\\xampp\\xampp-control.exe')      
    
# defines the file to save the apps employee profiles to. File can be loaded later
DATA_FILE = '..\\Employees.dat'
    
# create instance of MyGUI class
my_gui = MyGUI() 
