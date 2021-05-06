

class Login:

    '''This class allows you to enter: 
    the web address (URL) of the vestiaire page to be analyzed; 
    the email and password of the user for login; 
    and finally the number of pages to be analyzed.'''
    
    
    def __init__(self):
        
        self.link_page = self.url()
        self.profile, self.password, self.question = self.login_profile()
        self.pages = self.pages_to_be_analyzed()
    
    
    def url(self):
        '''Function to insert the web address (url) of the page with the price tables etc.'''

        while True:

            link_page = input("\nEnter the page address: ")
            break
        
        print('\nIf the program does not find the page, I advise you to check that the copied address is correct and restart the program.')
        
        return link_page
    
    
    def login_profile(self, *args):
        '''Function for entering the email and password to access the profile'''

        while True:

            profile = input("\nPut your profile email: ")
            password = input("\nEnter your profile password: ")
        
            print("\nLittle check of what you wrote --> [ {} ] -- [ {} ].".format(profile, password))
            
            question = input("\nWrite <v> if you want to continue or <x> if you want to write the email and password again: ")

            if question == "v":
                break
            
            elif question == "x":
                print("\nReceived! rewrite your email and password.")
            
            elif question != "v" and question != "x":
                print("\nMake sure you have written <v> and <x> correctly.")
                question = input("\nWrite <v> if you want to continue or <x> if you want to write the email and password again: ")
                
        
        return profile, password, question

    
    def pages_to_be_analyzed(self):
        '''Function to insert the number of pages to be analyzed in "orders and sales"'''


        while True:
            
            global pages
            
            try:
                pages = int(input("\nNow you have to enter the pages you want to analyze in the table of items sold in the orders and sales section: "))
                pages = pages + 1

            except ValueError:
                print("\nError - Careful! You don't have to enter a number in letters!")
            
            else:
                break
        
        print('\nWell done!')
        
        return pages



