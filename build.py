import os
import time
import shutil

current_dir = os.path.dirname(os.path.abspath(__file__))

def __clean():
    # if dist directory already exists, do a clean
    dist_dir = os.path.join(current_dir, 'dist')

    if os.path.exists(dist_dir):
        shutil.rmtree(dist_dir)

def __create_exe():
    output_dir = os.path.join(current_dir, 'dist', 'app')  # Specify the output directory

    cmd = (
        f'pyinstaller --upx-dir=C:\\upx-4.0.2-win64 --noconsole --onefile '
        f'--distpath="{output_dir}" '  # Set the output directory
        f'{current_dir}/src/Employee_Gui.py {current_dir}/src/Employee_Management_System.py '
        f'--icon={current_dir}/res/icon.ico --name "Employee Manager.exe"'
    )

    os.system(cmd)

def __move_res_files():
    output_dir = os.path.join(current_dir, 'dist')  # Specify the output directory

    # create the 'res' folder in the 'dist' directory if it doesn't exist
    res_dir = os.path.join(output_dir, 'res')
    os.makedirs(res_dir, exist_ok=True)

    # copy the 'res/icon.png' file into the 'res' folder
    icon_src = os.path.join(current_dir, 'res', 'icon.png')
    icon_dest = os.path.join(res_dir, 'icon.png')
    shutil.copy(icon_src, icon_dest)

def __build():
    ''' custom build file that converts the python src code to a single (distributable) executable file '''

    start_time = time.time() # start time tracker

    # set current system file and directory location for displaying file location info
    current_file = os.path.basename(__file__)
    print(f"Buildfile: {os.path.join(current_dir, current_file)}")

    __clean()

    print("create-Employee Manager.exe")

    __create_exe()

    __move_res_files()

    print("BUILD SUCCESSFUL")

    end_time = time.time() # end time tracker
    execution_time = end_time - start_time # calculate execution time
    print(f"Total time: {execution_time:.2f} seconds")

__build()
