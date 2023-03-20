import os, shutil
import plistlib
import sqlite3

###################################################### Basic functions
def file_copy(fileA,fileb):
    shutil.copy2(fileA, fileb)

def temp_folder_creation(folderName):
    if os.path.exists(folderName):
        shutil.rmtree(folderName)
    os.makedirs(folderName)

def check_file_in_folder(path_dir):
    filelist = os.listdir(path_dir)
    return filelist

def plistparser(fullpath):
    with open(fullpath, 'rb') as fp:
        return plistlib.load(fp)

def sqliteparser(fullpath):
    conn = sqlite3.connect(fullpath)
    return conn.cursor()
