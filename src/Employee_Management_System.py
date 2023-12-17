'''
Author @ Brian Perel
Employee_Management_System class, structured to store and return info
on employees stored in employee dictionary stored in GUI.py
'''

class Employee_Management_System:

    #print(__doc__)
    def __init__(self, id_number, name, department, title, pay_rate, phone_number, work_type):
        self.__id_number = id_number
        self.__name = name
        self.__department = department
        self.__title = title
        self.__pay_rate = pay_rate
        self.__phone_number = phone_number
        self.__work_type = work_type

    def set_id_number(self, id_number):
        self.__id_number = id_number

    def set_name(self, name):
        self.__name = name

    def set_department(self, department):
        self.__department = department

    def set_title(self, title):
        self.__title = title

    def set_pay_rate(self, pay_rate):
        self.__pay_rate = pay_rate

    def set_phone_number(self, phone_number):
        self.__phone_number = phone_number

    def set_work_type(self, work_type):
        self.__work_type = work_type

    def get_id_number(self):
        return self.__id_number

    def get_name(self):
        return self.__name

    def get_department(self):
        return self.__department

    def get_title(self):
        return self.__title

    def get_pay_rate(self):
        return self.__pay_rate

    def get_phone_number(self):
        return self.__phone_number

    def get_work_type(self):
        return self.__work_type

    def __str__(self):
        return 'ID number: ' + self.get_id_number() + \
                 '\nName: ' + self.get_name() + \
                 '\nDepartment: ' + self.get_department() + \
                 '\nTitle: ' + self.get_title() + \
                 '\nPay rate: ' + self.get_pay_rate() + \
                 '\nPhone number: ' + self.get_phone_number() + \
                 '\nEmployee Type: ' + self.get_work_type()
