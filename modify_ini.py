from configparser import ConfigParser
import sys


def select_account():
    '''Function where to enter the account name to change it'''

    global acc_name

    config = ConfigParser()
    config.read(r'C:\Users\Utente\Desktop\Vestiaire Folder\vestiaire_ini.ini')    
    sections = config.sections()

    for item_acc in sections:
        if item_acc.startswith('ACC'):
            print('\nAccounts --> ', item_acc)
            print(config[item_acc]['User email'])
            print(config[item_acc]['Status'])


    while True:

        acc_name = input('\nEnter the name of the account you want to change: ')

        if acc_name not in sections:
            print('\nCareful, the name you entered is not present in the file. Make sure you have spelled the account name correctly.')
        else:
            break
    
    return acc_name



def modify_ini():
    '''Function where you modify the data inside the ini file'''


    config = ConfigParser()
    config.read(r'C:\Users\Utente\Desktop\Vestiaire Folder\vestiaire_ini.ini')
    config.sections()

    print('\nEmail = ', config[acc_name]['User email'])
    print('URL site = ', config[acc_name]['URL site'])
    print('Languge = ', config[acc_name]['Language'])
    print('Account status = ', config[acc_name]['Status'])


    while True:

        options = input('''\nHi, here you can change your current account.
\nEnter "e" to edit the e-mail.
Enter "u" to change the url of the sales data page.
Enter 'la' to change the language.
Enter 's' to change the status of the account.
Enter "all" to change both.
Insert: ''')


        if options == 'e':   #'e' stands for e-mail

            user_email = input('\nEnter the new url of the page with the price tables: ')
            print("\nLittle check of what you wrote --> [ {} ]".format(user_email))

            config.set(acc_name, 'User email', user_email)
            with open(r'C:\Users\Utente\Desktop\Vestiaire Folder\vestiaire_ini.ini', 'w') as file:
                config.write(file)
            break
            

        elif options == 'u':   #'u' stands for URL

            link_page = input('\nEnter the url of the page with the price tables: ')
            print("\nLittle check of what you wrote --> [ {} ]".format(link_page))

            config.set(acc_name, 'URL site', link_page)
            with open(r'C:\Users\Utente\Desktop\Vestiaire Folder\vestiaire_ini.ini', 'w') as file:
                config.write(file)
            break


        elif options == 'la':   #'la' stands for language

            new_lang = input('Enter the new language: ')
            print("\nLittle check of what you wrote --> [ {} ]".format(new_lang))

            config.set(acc_name, 'Language', new_lang)
            with open(r'C:\Users\Utente\Desktop\Vestiaire Folder\vestiaire_ini.ini', 'w') as file:
                config.write(file)
            break


        elif options == 's':   #'s' stands for status

            print("\nEnter 'active' to activate the account, or 'disabled' to deactivate it.")

            for item_acc in config.sections():
                if item_acc.startswith('ACC'):
                    print('\nAccounts --> ', item_acc)
                    print(config[item_acc]['User email'])
                    print(config[item_acc]['Status'])

            while True:

                acc_status = input('\nChange your account status to activate or deactivate it: ')

                if acc_status == 'active' or acc_status == 'disabled':
                    print('\nwell done!')
                    break
                else:
                    print('\nCareful! the word you entered --> {} <-- is incorrect.'.format(acc_status))
            
            for item_acc in config.sections():
                if item_acc.startswith('ACC'):
                    config.set(item_acc, 'Status', 'disabled')


            config.set(acc_name, 'Status', acc_status)
            with open(r'C:\Users\Utente\Desktop\Vestiaire Folder\vestiaire_ini.ini', 'w') as file:
                config.write(file)
            break


        elif options == 'all':

            user_email = input('\nEnter the new url of the page with the price tables: ')
            link_page = input('\nEnter the url of the page with the price tables: ')
            new_lang = input('\nEnter the new language: ')
            print("\nLittle check of what you wrote --> [ {} ] -- [ {} ] -- [ {} ]".format(user_email, link_page, new_lang))


            config.set(acc_name, 'User email', user_email)
            config.set(acc_name, 'URL site', link_page)
            config.set(acc_name, 'Langiuage', new_lang)
            with open(r'C:\Users\Utente\Desktop\Vestiaire Folder\vestiaire_ini.ini', 'w') as file:
                config.write(file)
            break
            
        elif options != "u" or options != "e" or options != 'la' or options != 's' or options != "all":
            print("\nCareful, the command you entered is incorrect.\n'e' -> email,\n'u' -> site URL,\n'la --> language,\n 's' --> status active/disabled,\n'all' -> both.")



def check_status():
    '''Function that checks the status of accounts to prevent too many active ones.'''

    config = ConfigParser()
    config.read(r'C:\Users\Utente\Desktop\Vestiaire Folder\vestiaire_ini.ini')    
    sections = config.sections()

    count = 0
    for item in sections:
        if item.startswith('ACC'):
            if config[item]['Status'] == 'active':
                count += 1
    if count == 1:
        print('\nWell done!')
    else:
        print('You have too many active accounts !!! You can only leave one active.')
        sys.exit()





