import tkinter as tk
import logging

class Employee_Gui:

    def __init__(self, logger, db):
        self.logger = logger
        self.logger = logging.getLogger(__name__)

        self.__create_gui(db)
        db.check_db_size(gui=self)

        self.clear_gui_entry_fields()
        self.main_window.mainloop()

    def __create_gui(self, db):
        ''' create and place main gui window, buttons, labels, entry's, and a canvas1 line '''

        self.main_window = tk.Tk()  # make the GUI window

        try:
            self.main_window.iconphoto(True, tk.PhotoImage(file='../res/icon.png'))
        except (FileNotFoundError, tk.TclError) as e:
            self.logger.error(f"An error occurred while loading icon file: {e}")

        self.main_window.configure(background='lightgrey')  # app (GUI) background color
        self.main_window.title('EMS')  # app title
        self.main_window.resizable(0, 0)  # disable resizable option for GUI

        # launches the GUI in the center of the screen regardless of your screen resolution
        self.main_window.geometry(f'{520}x{420}+{((self.main_window.winfo_screenwidth() - 520) // 2)}+{((self.main_window.winfo_screenheight() - 420) // 2)}')

        # listens for when 'x' exit button is pressed and routes to __close_app
        self.main_window.protocol('WM_DELETE_WINDOW', lambda: db.close_app(self.main_window))

        # create a GUI label (display EMPLOYEE MANAGEMENT SYSTEM) = the header_label of the GUI app
        self.header_label = tk.Label(text='EMPLOYEE MANAGEMENT SYSTEM',
                    font='Times 12 bold', bg='lightgrey')

        # build line between header_label and the body of app
        self.header_canvas = tk.Canvas(self.main_window, width=495)

        # create line between header_label and body of app
        self.header_canvas.create_line(2, 25, 800, 25, width=2)

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
        self.id_output_entry = tk.Entry(textvariable=self.output_entry_var1)

        # sets focus on the first text field in app on startup
        self.id_output_entry.focus_set()

        # GUI button 1
        self.look_up_emp_button = tk.Button(text='Look Up Employee',
                    command=lambda: db.look_up_employee(gui=self), bg='SystemButtonFace')

        # create label
        self.enter_name_label = tk.Label(text='\tName:', font=('Courier', 10), bg='lightgrey')

        # take entry box variable and perform action
        self.name_output_entry = tk.Entry(textvariable=self.output_entry_var2)

        # GUI button (update employee)
        self.update_emp_button = tk.Button(text='Update Employee', command=lambda: db.update_employee(gui=self))

        self.enter_dept_label = tk.Label(text='\tDepartment:', font=('Courier', 10), bg='lightgrey')

        # take entry box variable and perform action
        self.dept_output_entry = tk.Entry(textvariable=self.output_entry_var3)

        # GUI buttons (delete employee)
        self.delete_emp_button = tk.Button(text='Delete Employee', command=lambda: db.delete_employee(gui=self))

        # display formatted label
        self.enter_title_label = tk.Label(text='\tTitle:', font=('Courier', 10), bg='lightgrey')

        # take entry box variable and perform action
        self.job_title_output_entry = tk.Entry(textvariable=self.output_entry_var4)

        # Opens XAMPP's MySQL module's admin website via weblink
        self.visit_db_button = tk.Button(text='Visit Database', font=('Courier', 10), borderwidth=3, cursor='hand2', command=db.open_db_website)

        # take entry box variable and perform action
        self.pay_rate_output_entry = tk.Entry(textvariable=self.output_entry_var5)

        self.reset_button_canvas = tk.Canvas(self.main_window, width=195)

        self.reset_button_canvas.create_line(2, 25, 600, 25, width=2)

        # display formatted label
        self.enter_pay_rate_label = tk.Label(text='\tPay Rate:', font=('Courier', 10), bg='lightgrey')

        # display formatted label
        self.enter_phone_num_label = tk.Label(text='\tPhone Number:', font=('Courier', 10), bg='lightgrey')

        self.phone_num_output_entry = tk.Entry(textvariable=self.output_entry_var6)

        # GUI formatted buttons, call appropriate method when clicked
        self.reset_button = tk.Button(text='Reset System', command=lambda: db.reset_system(gui=self))

        # reset radio button variable to blank option (0)
        self.radio_var.set(0)

        # create radio button
        self.part_time_rb1 = tk.Radiobutton(text='Part Time Employee', variable=self.radio_var,
                                    bg='lightgrey', value=1, cursor='hand2')

        # create radio button
        self.full_time_rb2 = tk.Radiobutton(text='Full Time Employee', variable=self.radio_var,
                                    bg='lightgrey', value=2, cursor='hand2')

        # GUI button
        self.add_emp_button = tk.Button(text='Add New Employee', command=lambda: db.add_employee(gui=self))

        # build line between body of app and footer_label
        self.footer_canvas = tk.Canvas(self.main_window, width=495)

        # create line between body of app and footer_label
        self.footer_canvas.create_line(2, 25, 600, 25, width=2)

        # display formatted label in app
        self.footer_label = tk.Label(text='created by Brian Perel', font=('Courier', 10), bg='lightgrey')

        # make program position and display all gui components (widgets)
        self.header_label.place(x=120, y=2)
        self.header_canvas.place(x=10, y=20)
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
        self.part_time_rb1.place(x=240, y=307)
        self.full_time_rb2.place(x=380, y=307)
        self.visit_db_button.place(x=10, y=225)
        self.reset_button_canvas.place(x=10, y=258)
        self.reset_button.place(x=10, y=307)
        self.footer_canvas.place(x=10, y=340)
        self.footer_label.place(x=160, y=380)

        for button in [self.look_up_emp_button, self.add_emp_button, self.update_emp_button,
                   self.delete_emp_button, self.reset_button]:
            button.config(font=('Courier', 10), borderwidth=3, cursor='hand2')
            button.bind('<Enter>', self.__on_hover)
            button.bind('<Leave>', self.__on_leave)

        for canvas in [self.header_canvas, self.reset_button_canvas, self.footer_canvas]:
            canvas.config(height=40, bd=0, borderwidth=0, bg='lightgrey', highlightthickness=0.5, highlightbackground='lightgrey')

        for entry in [self.id_output_entry, self.name_output_entry, self.dept_output_entry, self.job_title_output_entry,
                          self.pay_rate_output_entry, self.phone_num_output_entry]:
            # if user clicks in this text field box with their mouse, call this function
            entry.bind('<Button-1>', self.__on_click)
            # if user clicks in this text field box with their keyboard, call this function
            entry.bind('<FocusIn>', self.__on_click)
            # if insertion pointer leaves current text field (focus is lost) call this function
            entry.bind('<FocusOut>', lambda event, entry=entry: self.__focus_out(event, entry))
            entry.config(width=15, font=('Courier', 10), bd=2, highlightthickness=1, highlightcolor='black', foreground='grey', validate="key", validatecommand=(self.main_window.register(self.__validate_entry), '%P'))

        self.tooltip = None
        self.visit_db_button.bind("<Enter>", lambda event, button=self.visit_db_button: self.schedule_tooltip(event, button))
        self.visit_db_button.bind("<Leave>", lambda event: self.hide_tooltip(event))

    def __validate_entry(self, value):
        # only allow up to 6 characters in ID or pay rate and up to 12 characters in name, dept, job title, or phone number fields
        if self.main_window.focus_get() == self.id_output_entry or self.main_window.focus_get() == self.pay_rate_output_entry:
            return len(value) <= 6
        elif self.main_window.focus_get() in [self.name_output_entry, self.dept_output_entry,
                                              self.job_title_output_entry, self.phone_num_output_entry]:
            return len(value) <= 12
        else:
            return True

    def clear_gui_entry_fields(self):
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
            entry.config(foreground='grey', validate="key", validatecommand=(self.main_window.register(self.__validate_entry), '%P'))

    def __on_hover(self, event):
        ''' when user hovers over a button, the button's background color and border width are changed to what is specified below
        '''
        event.widget.config(bg='lightgrey', borderwidth=3.8)

    def __on_leave(self, event):
        ''' when user stops hovers over a button, the button's background color and border width are changed to default values
        '''
        event.widget.config(bg='SystemButtonFace', borderwidth=3)

    def __on_click(self, event):
        ''' erases the auto inserted GUI startup entry box text
        '''

        # sets the entry box's text to be black and deletes existing text
        event.widget.config(foreground='black')

        if event.widget.get() in ['Enter id...', 'Enter name...', 'Enter dept...', 'Enter title...', 'Enter pay...', 'XXX-XXX-XXXX']:
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
        entry_widget.config(foreground='grey', validate="key", validatecommand=(self.main_window.register(self.__validate_entry), '%P'))

    def schedule_tooltip(self, event, button):
        # make the button become it's hover state style
        event.widget.config(bg='lightgrey', borderwidth=3.8)
        self.tooltip_id = self.visit_db_button.after(1500, lambda: self.show_tooltip(button))

    def show_tooltip(self, button):
        if self.tooltip_id:
            self.visit_db_button.after_cancel(self.tooltip_id)
            self.tooltip_id = None

            x, y, _, _ = button.bbox("insert")

            # Create a toplevel window
            self.tooltip = tk.Toplevel(button)
            self.tooltip.wm_overrideredirect(True)
            self.tooltip.wm_geometry(f"+{x+button.winfo_rootx() + 30}+{y+button.winfo_rooty() + 38}")

            # Display the tooltip text
            label = tk.Label(self.tooltip, text="http://localhost/phpmyadmin/index.php?route=/sql&server=1&db=company&table=employees", background="#ffffe0", relief="solid", borderwidth=1)
            label.pack(ipadx=1)

    def hide_tooltip(self, event):
        # make the button become it's regular (non-hover state) style
        event.widget.config(bg='SystemButtonFace', borderwidth=3)

        if self.tooltip_id:
            self.visit_db_button.after_cancel(self.tooltip_id)
            self.tooltip_id = None
        if self.tooltip:
            self.tooltip.destroy()
            self.tooltip = None