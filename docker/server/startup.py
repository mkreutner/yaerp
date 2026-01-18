#!/usr/bin/env python

import os.path
import subprocess
import sys

def install(package: str) -> None:
    '''
    Install the package
    
    :param package: package name
    :type package: str
    '''
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

def is_installed(package: str) -> bool:
    '''
    Checks if package is installed
    
    :param package: package name
    :type package: str
    :return: True if package is found, False otherwise
    :rtype: bool
    '''
    return package in sys.modules.keys()

if __name__ == '''__main__''':

    # 0. Update pip
    is_new_install = False
    is_new_project = False
    subprocess.run(["pip", "install", "--upgrade", "pip"])

    # 1. Check Django and install it if needed.
    if is_installed("django") != True:
        # Install Django
        install("django")
        is_new_install = True
    
    # Update Path
    home = os.path.expanduser("~")
    sys.path.append(os.path.join(home, ".local", "bin"))

    # 2. Check in porject is already create
    if os.path.exists("./manage.py") != True:
        # Project not yet initialized
        # Retreive current folder name and use it to initialize project
        # The project takes the name of the current path
        path, project_name = os.path.split(os.path.realpath(os.getcwd()))
        subprocess.run([os.path.join(home, ".local", "bin", "django-admin"), "startproject", "core", "."])
        is_new_project = True
    
    if is_new_install == True & is_new_project == True:
        # Create requirements
        subprocess.run(["pip", "freeze", ">", "requirements.txt"])
    elif is_new_install == True & is_new_project == False:
        # Install requirements
        if os.path.exists("requirements.txt") != True:
            subprocess.run(["pip", "insall", "-r", "requirements.txt"])
    else:
        # Update requirements
        subprocess.run(["pip", "freeze", ">", "requirements.txt"])

    # 4. Run the project 
    subprocess.run(["python", "manage.py", "runserver", "0.0.0.0:8000"])

