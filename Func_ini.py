from configparser import ConfigParser
import language as la



def add_user_email():
        '''Function for entering user email to the ini file '''

        global user_email
        
        user_email = input('\nEnter your email account: ')
        print("\nLittle check of what you wrote --> [ {} ]".format(user_email))
        
        return user_email
    


def email_check():
    '''Function that verifies the user's email'''

    while True:
        
        question = input("\nWrite <v> if you want to continue or <x> if you want to write the email again: ")

        if question == "v":
            break
        
        elif question == "x":
            print("\nReceived! rewrite your email.")
            add_user_email()
        
        elif question != "v" and question != "x":
            print("\nMake sure you have written <v> and <x> correctly.")



def siteURL():
    '''Function to insert the URL of the page with the sales data'''

    global link_page

    print('''\nTo get started, go to Vestiaire Collective and click on your profile photo.
Then click again on -> my items for sale <- and click again on -> orders and sales <-.
At this point, copy the page address or URL.
Now paste the address in the space provided
and conclude by pressing enter again and subsequently entering the other data to complete the operation.''')
    
    link_page = input('\nEnter the url of the page with the price tables: ')
    
    return link_page

    
    
def site_language():
    '''Function where to enter the language'''

    global user_lang


    while True:

        user_lang = input('''\nSelect the language you use on the Vestiaire website by putting the two letters that identify it.
    \nHere are some examples:
    English -> 'en';
    French -> 'fr';
    German -> 'de';
    Italian -> 'it';
    Danish -> 'da'.
    Insert: ''')
        if user_lang not in la.LANGUAGES.keys():
            print('\nThe language you entered is incorrect ... check that the two letters represent the language well.')
        else:
            break

    return user_lang



def add_acc_ini():
    '''Function where to add a new account to the ini file'''

    config = ConfigParser()

    choose_name = input('\nChoose the name of the new account: ')
    print("\nLittle check of what you wrote --> [ {} ]".format(choose_name))

    config[choose_name] = {
        'User email': user_email,
        'URL site': link_page,
        'Language': user_lang
    }

    with open(r'C:\Users\Utente\Desktop\Vestiaire Folder\vestiaire_ini.ini', 'a') as file:
        config.write(file)


def name_acc_check():
    '''Function that verifies the user's email'''

    while True:
        
        question = input("\nWrite <v> if you want to continue or <x> if you want to write the name of the account again: ")

        if question == "v":
            break
        
        elif question == "x":
            print("\nReceived! rewrite your account name.")
            add_acc_ini()
        
        elif question != "v" and question != "x":
            print("\nMake sure you have written <v> and <x> correctly.")


