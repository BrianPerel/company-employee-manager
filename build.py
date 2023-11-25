import os
import time
import glob
import shutil

current_dir = os.path.dirname(os.path.abspath(__file__))

def __clean():
    # if dist or build directories already exists, do a clean
    dist_dir = os.path.join(current_dir, 'dist')
    build_dir = os.path.join(current_dir, 'build')

    if os.path.exists(dist_dir):
        shutil.rmtree(dist_dir)

    if os.path.exists(build_dir):
        shutil.rmtree(build_dir)

def __create_exe():
    output_dir = os.path.join(current_dir, 'dist', 'app')  # Specify the executable output directory path ('dist/app/')
    source_files = glob.glob(os.path.join(current_dir, 'src', '*.py'))  # get a list of all Python files in the src directory

    cmd = (
        f'start /min cmd /c pyinstaller --upx-dir=C:\\upx-4.0.2-win64 --noconsole --onefile ' # call the pyinstaller to package the python scripts using upx packager
        f'--distpath="{output_dir}" '  # set the output directory for generated exe
        f'{" ".join(source_files)} ' # include all Python scripts from the src directory
        f'--icon={current_dir}/res/icon.ico --name "Employee Manager.exe"' # include the icon file which will appear as the custom file icon, and assign a name to the exe
    )

    os.system(cmd)

    # added a wait here so that the above command prompt commands execute before other code outside this function is executed
    time.sleep(8)

def __move_res_files():
    output_dir = os.path.join(current_dir, 'dist')  # specify the output directory for the generated exe

    # create the 'res' folder in the 'dist' directory if it doesn't exist
    res_dir = os.path.join(output_dir, 'res')
    os.makedirs(res_dir, exist_ok=True)

    # copy the 'res/icon.png' file into the exe output dir under subfolder 'res'
    icon_src = os.path.join(current_dir, 'res', 'icon.png')
    icon_dest = os.path.join(res_dir, 'icon.png')
    shutil.copy(icon_src, icon_dest)

def __build():
    ''' custom build file that converts the python src code to a single packaged (distributable) executable file '''

    start_time = time.time() # start script time tracker

    # set current system file and directory location for displaying file location info
    current_file = os.path.basename(__file__)
    print(f"Buildfile: {os.path.join(current_dir, current_file)}")

    __clean()

    print("create-Employee Manager.exe")

    __create_exe()

    __move_res_files()

    file_path = "Employee Manager.exe.spec"

    try:
        os.remove(file_path)
        print(f"The file '{file_path}' has been successfully deleted.")
    except FileNotFoundError:
        print(f"The file '{file_path}' does not exist.")
    except PermissionError:
        print(f"Permission error: Unable to delete the file '{file_path}'.")
    except Exception as e:
        print(f"An error occurred: {e}")

    print("BUILD SUCCESSFUL")

    end_time = time.time() # end script time tracker
    execution_time = end_time - start_time # calculate execution time
    print(f"Total time: {execution_time:.2f} seconds")

__build()
