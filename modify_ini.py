from configparser import ConfigParser
import language 


def select_account():
    '''Function where to enter the account name to change it'''

    global acc_name

    config = ConfigParser()
    config.read(r'C:\Users\Utente\Desktop\Vestiaire Folder\vestiaire_ini.ini')    
    sections = config.sections()
    print('\nHere are the sections of the ini file ->', sections)

    while True:

        acc_name = input('\nEnter the name of the account you want to change: ')

        if acc_name not in sections:
            print('\nCareful, the name you entered is not present in the file. Make sure you have spelled the account name correctly.')
        else:
            print('Well done!')
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


    while True:

        options = input('''\nHi, here you can change your current account.
\nEnter "e" to edit the email.
Enter "u" to change the url of the sales data page.
Enter 'la' to change the language.
Enter "all" to change both.
Insert: ''')

        if options == 'e':

            user_email = input('\nEnter the new url of the page with the price tables: ')
            print("\nLittle check of what you wrote --> [ {} ]".format(user_email))

            config.set(acc_name, 'User email', user_email)
            with open(r'C:\Users\Utente\Desktop\Vestiaire Folder\vestiaire_ini.ini', 'w') as file:
                config.write(file)
            break
            

        elif options == 'u':

            link_page = input('\nEnter the url of the page with the price tables: ')
            print("\nLittle check of what you wrote --> [ {} ]".format(link_page))

            config.set(acc_name, 'URL site', link_page)
            with open(r'C:\Users\Utente\Desktop\Vestiaire Folder\vestiaire_ini.ini', 'w') as file:
                config.write(file)
            break

        elif options == 'la':
            new_lang = input('Enter the new language: ')
            print("\nLittle check of what you wrote --> [ {} ]".format(new_lang))

            config.set(acc_name, 'Language', new_lang)
            with open(r'C:\Users\Utente\Desktop\Vestiaire Folder\vestiaire_ini.ini', 'w') as file:
                config.write(file)
            break


        elif options == 'all':

            user_email = input('\nEnter the new url of the page with the price tables: ')
            link_page = input('\nEnter the url of the page with the price tables: ')
            new_lang = input('\nEnter the new language: ')
            print("\nLittle check of what you wrote --> [ {} ] -- [ {} ]".format(user_email, link_page, new_lang))


            config.set(acc_name, 'User email', user_email)
            config.set(acc_name, 'URL site', link_page)
            config.set(acc_name, 'Langiuage', new_lang)
            with open(r'C:\Users\Utente\Desktop\Vestiaire Folder\vestiaire_ini.ini', 'w') as file:
                config.write(file)
            break
            
        elif options != "u" or options != "e" or options != 'la' or options != "all":
            print("\nCareful, the command you entered is incorrect.\n'e' -> email,\n'u' -> site URL,\n'la --> language,\n'all' -> both.")

