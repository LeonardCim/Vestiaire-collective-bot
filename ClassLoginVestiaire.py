

class Login:

    'This class allows you to enter: the password of the user for login'
    
    
    def __init__(self):
        
        self.password, self.question = self.login_profile()
    
    
    def login_profile(self, *args):
        '''Function for entering the password to access the profile'''

        while True:

            password = input("\nEnter your profile password: ")
        
            print("\nLittle check of what you wrote --> [ {} ].".format(password))
            
            question = input("\nWrite <v> if you want to continue or <x> if you want to write the password again: ")

            if question == "v":
                break
            
            elif question == "x":
                print("\nReceived! rewrite your password.")
            
            elif question != "v" and question != "x":
                print("\nMake sure you have written <v> and <x> correctly.")
                question = input("\nWrite <v> if you want to continue or <x> if you want to write password again: ")
                
        
        return password, question




