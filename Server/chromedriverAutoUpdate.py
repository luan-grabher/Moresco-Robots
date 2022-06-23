import shutil
from pathlib import Path


def up_one_dir(path):
    try:
        # from Python 3.6
        parent_dir = Path(path).parents[1]
        
        shutil.move(path, parent_dir)
    except IndexError:
        # no upper directory
        pass

import chromedriver_autoinstaller as installer
import os

'''
    TESTING
'''
#Get desktop path of user
#desktop_path = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
#set path = to desktop path
#path = desktop_path

'''
    FINAL
'''
path = '\\\\heimerdinger\\docs\\Informatica\\Programas\\Moresco\\Selenium WebDriver\\Chromedriver'

#with chrome driver auto update, download and save on desktop
install_file = installer.install(path = path)

#get parent of parent of install file
moved_dir = Path(install_file).parents[1]
#if moved_dir folder has a file 'chromedriver.exe', delete it
if os.path.isfile(os.path.join(moved_dir, 'chromedriver.exe')):
    os.remove(os.path.join(moved_dir, 'chromedriver.exe'))

#up file to one directory up
up_one_dir(install_file)

#get parent directory of install file
parent_dir = Path(install_file).parents[0]
#remove parent directory
shutil.rmtree(parent_dir)

