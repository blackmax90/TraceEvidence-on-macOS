from Modules.TEFT_Define import *
from termcolor import colored

def run_tool():
    os.system('cls')
    f = Figlet(font='big')
    print(colored(f.renderText('< TEFT >\n             - MS OFFICE'), 'magenta'))
    print(colored("Trace Evidence Forensics Tool\n\n", 'blue'))

def select_input():
    while True:
        print(colored("|################## I.N.P.U.T #################|", 'cyan'))
        print(colored("|   1. Live System                             |", 'cyan'))
        print(colored("|   2. Disk Image                              |", 'cyan'))
        print(colored("|   3. Directory (for testing purposes)        |", 'cyan'))
        print(colored("|##############################################|", 'cyan'))
        print()
        inputType = input("Select Input: ")
        if int(inputType) == 1 or int(inputType) == 3:
            return inputType
        elif int(inputType) == 2:
            print()
            print(colored("> In development...", 'yellow'))
            print(colored("> Please select another input type\n", 'yellow'))
        else:
            print()
            print(colored("> Please type a correct number (1~3)\n", 'yellow'))

def type_source_path():
    while True:
        print(colored("|################## P.A.T.H ###################|", 'cyan'))
        print(colored("|    ex) /Users/[Account]/Desktop/source       |", 'cyan'))
        print(colored("|    ex) D:/source                             |", 'cyan'))
        print(colored("|    ex) For testing, type 'SampleDataSet'      |", 'cyan'))
        print(colored("|##############################################|", 'cyan'))
        print()
        inputType = input("Please type the source folder (absolute path): ")
        if os.path.isdir(inputType) == True:
            return inputType
        else:
            print()
            print(colored("> Please type a correct path\n", 'yellow'))

def type_user_name(sourceFolder):
    while True:
        print(colored("|################## U.S.E.R ###################|", 'cyan'))
        print(colored("|    ex) max                                   |", 'cyan'))
        print(colored("|    ex) david                                 |", 'cyan'))
        print(colored("|    ex) x (if you don't know the user name)   |", 'cyan'))
        print(colored("|##############################################|", 'cyan'))
        print()
        UserName = input("Please type the user name: ")
        if os.path.isdir(sourceFolder+'/Users/'+UserName) == True:
            return UserName
        elif UserName == 'x':
            return UserName
        else:
            print()
            print(colored("> Please type a correct user name or type 'x'\n", 'yellow'))