from configparser import ConfigParser
import create_ini as ci
import shutil
import sys
import os



#This script runs only once at the beginning of the program. Then it will no longer be used.

count = 0

while True:

    def vestiaire_folder(folder_name):
        '''Function to create the Vestiaire folder with inside the csv file with all the data and the ini file'''

        global make_folder
        global ves_folder

        desktop_path = r'C:\Users\Utente\Desktop'
        ves_folder = os.path.join(desktop_path, folder_name)

        try:
            make_folder = os.mkdir(ves_folder)
            
        except FileExistsError:
            print('''\nCareful, it seems that another folder has the same name as this one --> "Vestiaire Folder"
To make the program work correctly you have to change the name of the folder that already exists.''')
            sys.exit()

        return make_folder, ves_folder


    def driver():
        '''Function where to enter the path of the webdriver'''
        
        global driver_path

        print('''\n        Enter the path to the folder where the Webdriver is located. Example -> C: \ Users \ User\Desktop\ "folder name"
        Obviously with no space between the bars.
        If there is any error after entering the path, 
        delete the folder that has just been created (Vestiaire Folder) 
        and restart the program checking that you have copied the path correctly.''')

        path = r'C:\Users\Utente\Desktop\Vestiaire Folder'
        source_dir = str(input('\nEnter the path of the Webdriver: '))
        

        for file in os.listdir(source_dir):
            if file.endswith('.exe'):
                create = source_dir + '/' + file
                shutil.move(create, path)
    
        driver_path = r'C:\Users\Utente\Desktop\Vestiaire Folder\chromedriver.exe'

        return driver_path
    

    def check_path_exe():
        '''Function that controls the path of the webdriver'''

        while True:

            try: 
                driver()
                break
            
            except FileNotFoundError as ex:
                print('\nERROR --> {}'.format(ex))
                print('\nThe path you entered is incorrect ... check that it is written correctly.')
    
    count +=  1


    def ini():
        '''Creation function of the ini file with the data to make the bot work'''
        
        config = ConfigParser()

        config['SETTINGS'] = {
            'Chromedriver-PATH': driver_path,
            'count': count
        }

        config['ACCOUNT 0'] = {
            'User email': ci.user_email,
            'URL site': ci.link_page,
            'Language': ci.user_lang,
            'Status': 'active'
        }


        with open(os.path.join(ves_folder, 'vestiaire_ini.ini'), 'w+') as file:
            config.write(file)
    
    break
 

try:
    config = ConfigParser()
    config.read(r'C:\Users\Utente\Desktop\Vestiaire Folder\vestiaire_ini.ini')
    
    if config.get('SETTINGS', 'count') == '1':
        pass

except Exception:
    vestiaire_folder('Vestiaire Folder')
    ci.add_user_email()
    ci.email_check()
    ci.siteURL()
    ci.site_language()
    check_path_exe()
    ini()
    
    sys.exit()