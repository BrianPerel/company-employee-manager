from datetime import datetime
import logging
import os

class Employee_Logger:

    def setup_custom_logger(self):
        # create log folder if it doesn't exist
        os.makedirs("../log", exist_ok=True)

        # setup and configure a custom logger
        logger = logging.getLogger("employee_logger")

        cust_log_format ='%(asctime)s %(levelname)s %(funcName)s(): line %(lineno)d: - %(message)s'

        # create a console handler, set a custom formatter on the console handler, add the console handler to the logger
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(logging.Formatter(cust_log_format))
        logger.addHandler(console_handler)

        # create a file handler, set a custom formatter on the file handler to include current date in file name and be placed in log folder.
        # Add the file handler to the logger. Log file will override existing log file of same date
        file_handler = logging.FileHandler(os.path.join("../log", f'employee_manager.{datetime.now().strftime("%m_%d_%Y")}.log'), mode='w')
        logging.basicConfig(handlers=[file_handler], level=logging.INFO, format=cust_log_format)

        return logger