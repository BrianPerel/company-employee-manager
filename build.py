'''
Author: Brian Perel
Build script for building a standalone executable file using PyInstaller for the project.
Make sure to have pyinstaller installed in pip and optionally upx packager before running this script
'''

import pkg_resources
import subprocess
import shutil
import time
import glob
import os

DIST_DIR = 'dist'
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

def __clean():
    ''' removes the 'dist' and/or 'build' directories if they already exist
    '''

    dist_dir = os.path.join(CURRENT_DIR, 'dist')
    build_dir = os.path.join(CURRENT_DIR, 'build')

    if os.path.exists(dist_dir):
        shutil.rmtree(dist_dir)

    if os.path.exists(build_dir):
        shutil.rmtree(build_dir)

def __create_exe():
    ''' Creates the executable:
        Defines the output directory for the executable ('dist/app/').
        Retrieves a list of Python files in the 'src' directory.
        Utilizes the UPX packer for efficient packaging.
        Applies a custom exe output file name along with a custom icon file
        Constructs a command to run PyInstaller with specific options
    '''

    output_dir = os.path.join(CURRENT_DIR, 'dist', 'app')  # specify the executable output directory path ('dist/app/')
    source_files = glob.glob(os.path.join(CURRENT_DIR, 'src', '*.py'))  # get a list of all Python files in the src directory

    cmd = (
        f'start /min cmd /c pyinstaller --upx-dir=C:\\upx-4.0.2-win64 --noconsole --onefile ' # call the pyinstaller to package the python scripts using upx packager
        f'--distpath="{output_dir}" '  # set the output directory for the generated exe
        f'{" ".join(source_files)} ' # include all Python script files from the src directory
        f'--icon={CURRENT_DIR}/res/icon.ico --name "Employee Manager.exe"' # include the icon file which will appear as the custom file icon, and assign a name to the exe
    )

    try:
        subprocess.run(cmd, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error: Command returned non-zero exit code {e.returncode}")

    # added a wait time here so that the above command prompt commands execute before other code outside this function is executed
    time.sleep(8)

def __move_res_files():
    ''' Creates a 'res' folder in the 'dist' directory if it doesn't exist.
        Copies the 'res/icon.png' file into the 'dist/res' subfolder.
    '''

    # specify the output directory for the generated exe
    output_dir = os.path.join(CURRENT_DIR, 'dist')

    # create the 'res' folder in the 'dist' directory if it doesn't exist
    res_dir = os.path.join(output_dir, 'res')
    os.makedirs(res_dir, exist_ok=True)

    # copy the 'res/icon.png' file into the exe output dir under subfolder 'res'
    icon_src = os.path.join(CURRENT_DIR, 'res', 'icon.png')
    icon_dest = os.path.join(res_dir, 'icon.png')
    shutil.copy(icon_src, icon_dest)

def __move_exe_to_desktop():
    print("copying dist folder to the desktop")
     # move the 'dist' folder to the user's desktop
    desktop_path = os.path.join(os.path.expanduser('~'), 'Desktop')
    dist_dest = os.path.join(desktop_path, 'dist')

    try:
        # delete the existing 'dist' folder from the desktop if it already exists
        if os.path.exists(dist_dest):
            shutil.rmtree(dist_dest)

        # copy 'dist' folder to the desktop
        shutil.copytree(os.path.join(CURRENT_DIR, 'dist'), dist_dest)
        print(f"The 'dist' folder has been successfully copied to the desktop.")
    except FileNotFoundError:
        print("Error - The 'dist' folder does not exist.")
    except PermissionError:
        print("Permission error - Unable to move the 'dist' folder.")
    except Exception as e:
        print(f"An error occurred while moving the 'dist' folder: {e}")

def __build():
    ''' custom build file that converts the python src code to a single packaged (distributable) executable file '''

    # set current system file and directory location for displaying file location info
    current_file = os.path.basename(__file__)
    print(f"Buildfile: {os.path.join(CURRENT_DIR, current_file)}")

    __clean()

    print("creating Employee Manager.exe")

    __create_exe()

    __move_res_files()

    file_path = "Employee Manager.exe.spec"

    try:
        os.remove(file_path)
        print(f"The '{file_path}' file has been successfully deleted.")
    except FileNotFoundError:
        print(f"The file '{file_path}' does not exist.")
    except PermissionError:
        print(f"Permission error: Unable to delete the file '{file_path}'.")
    except Exception as e:
        print(f"An error occurred: {e}")

    # provide extra time to allow the current dist folder creation process to complete before copying directory to desktop
    time.sleep(2)

    __move_exe_to_desktop()

# only run the build script if the required pyinstaller package is installed. This check is needed because
# pyinstaller is called via command prompt, where the check is not implicitly done.
try:
    start_time = time.time() # start script execution time tracker

    pkg_resources.get_distribution('pyinstaller')
    __build()

    print("BUILD SUCCESSFUL")

    end_time = time.time() # end script execution time tracker
    execution_time = end_time - start_time # calculate total script execution time
    print(f"Total time: {execution_time:.2f} seconds")
except pkg_resources.DistributionNotFound:
    print("Error - pyinstaller is not installed. Please install Python pyinstaller package in pip")
