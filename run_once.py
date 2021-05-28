from configparser import ConfigParser
import shutil
import os


count = 0

while True:
    
    def vestiaire_folder(folder_name):
        '''Function to create the Vestiaire folder with inside: the csv file with all the data 
        and an additional file for the correct functioning of the program which must not be modified!!!
        (For example, there is the Webdriver inside)'''

        global make_folder
        global folder

        path = r'C:\Users\Utente\Desktop'
        folder = os.path.join(path, folder_name)
        make_folder = os.mkdir(folder)

        return make_folder, folder
   

    def driver():
        '''Function where to enter the path of the webdriver'''
        
        global new_path

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
        
        new_path = r'C:\Users\Utente\Desktop\Vestiaire Folder\chromedriver.exe'

        return new_path

    
    count +=  1

    def ini():
        '''Creation function of the ini file with the data to make the bot work'''
        
        config = ConfigParser()

        config['SETTINGS'] = {
            'Chromedriver-PATH': new_path,
            'count': count
        }

        with open(os.path.join(folder, 'vestiaire_ini.ini'), 'w+') as newfile:
            config.write(newfile)
    
    break


try:
    config = ConfigParser()
    config.read(r'C:\Users\Utente\Desktop\Vestiaire Folder\vestiaire_ini.ini')
    
    if config.get('SETTINGS', 'count') == '1':
        pass

except Exception as ex:
    print("\nError --> {} -- Go ahead, don't worry :-)".format(ex))
    vestiaire_folder('Vestiaire Folder')
    driver()
    ini()


