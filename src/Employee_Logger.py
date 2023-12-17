from datetime import datetime
import logging
import shutil
import os

class Employee_Logger:

    def setup_custom_logger(self):
        logs_deleted = False

        if os.path.exists("../log"):
            existing_log_files = [file for file in os.listdir("../log") if file.startswith("employee_manager") and file.endswith(".log")]

            if len(existing_log_files) > 15:
                shutil.rmtree("../log")
                logs_deleted = True

        # create log folder if it doesn't exist
        os.makedirs("../log", exist_ok=True)

        # setup and configure a custom logger
        logger = logging.getLogger("employee_logger")

        # create a file and console handler, set a custom formatter on the file and console handlers to include current date in file name and to be placed in log folder.
        # Add the file and console handlers to the logger. Log file will override existing log file of same date
        file_handler = logging.FileHandler(os.path.join("../log", f'employee_manager.{datetime.now().strftime("%m_%d_%Y")}.log'), mode='w')
        logging.basicConfig(handlers=[file_handler, logging.StreamHandler()], level=logging.INFO, format='%(asctime)s %(levelname)s %(funcName)s(): line %(lineno)d: - %(message)s')

        if logs_deleted:
            logger.info("More than 15 log files we're found - log folder deleted")

        return logger
