from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup as SOUP
from configparser import ConfigParser
from selenium import webdriver
import datetime
import shutil
import time
import csv
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




print('''\nTo get started, go to Vestiaire Collective and click on your profile photo.
Then click again on -> my items for sale <- and click again on -> orders and sales <-.
At this point, copy the page address or URL.
Now press enter and paste the address in the space provided
and conclude by pressing enter again and subsequently entering the other data to complete the operation.''')



from ClassLoginVestiaire import Login

link_page = Login.url("\nEnter the page address: ")
profile, password, question = Login.login_profile("\nPut your profile email: ", "\nEnter your profile password: ", "\nWrite <v> if you want to continue or <x> if you want to write the email and password again: ")
pages = Login.pages_to_be_analyzed("\nEnter the number of pages you want to analyze: ")



config = ConfigParser()

config.read(r'C:\Users\Utente\Desktop\Vestiaire Folder\vestiaire_ini.ini')
PATH = config.get('SETTINGS', 'Chromedriver-PATH')


try:
    driver = webdriver.Chrome(PATH)
    driver.get(link_page)

except Exception as ex:
    print("Error --> {} -- Restart the program.".format(ex))
    driver.quit()
    exit()
else:
    pass


try:
    cookie = WebDriverWait(driver, 15).until(
        EC.element_to_be_clickable((By.ID, 'popin_tc_privacy_button_2'))
        )
    cookie.click()

except TimeoutException:
    pass



def access():
    '''Small function with elements that log in to the profile.'''

    driver.find_element_by_id('loginEmail').send_keys(profile), time.sleep(1)
    driver.find_element_by_id('loginPassword').send_keys(password), time.sleep(1)
    driver.find_element_by_xpath('//*[@id="popin-signup"]/div/div/div[3]/div/form/p[2]/button').click()


    orders_and_sales = WebDriverWait(driver, 15).until(
        EC.element_to_be_clickable((By.ID, 'commandes_click'))
    )
    orders_and_sales.click()

access()



namedress = []
pricelist = []
date = []


def first_actions(i=None):
    '''Function to extract data from Vestiaire Collective'''

    for i in range(1, pages):

        html = driver.page_source
        soup = SOUP(html, 'html.parser')


        for name in soup.find_all('td', 'order-product'):
            namedress.append(str(" ".join(name.text.split())))


        for price in soup.find_all('td', 'order-amount'):
            pricelist.append(int(price.text.split(",")[0]))


        for dat in soup.select('div.product-item'):
            elements = dat.find_all('li')[-1]
            date.append(' '.join(elements.text.split()[2:]))

        for item in date:

            if item == '':
                inde = date.index(item)
                remove = date.pop(inde)
                insert = date.insert(inde, "Item not sold or shipping.")
            else:
                pass
        

        time.sleep(0.5)
        
        try:
            time.sleep(1)

            driver.execute_script("arguments[0].click();", WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "#sales_ezpgn > a.ezpgn.ezpgn_right"))))

            time.sleep(1)

            html = driver.page_source
            soup = SOUP(html, 'html.parser')

        except TimeoutException:
            pass
    
first_actions()

time.sleep(1)



real_prices = []

#is the basic commission for prices less than or equal to 150
com_base = 15

for num in pricelist:

    if num <= 150:
        real_prices.append(num - 15)

    elif num > 150 and num <= 210:
        real_prices.append(int(num * 0.85))

    elif num > 210 and num <= 300:
        a = (num-210)/10+com_base
        b = 100 - a
        c = b*0.01
        d = round(c, 2)
        e = num*d
        real_prices.append(int(e))

    elif num > 300 and num <= 2000:
        real_prices.append(int(num*0.75))

    elif num > 2000 and num <= 4000:
        real_prices.append(int(num*0.77))

    elif num > 4000 and num <= 5000:
        real_prices.append(int(num*0.78))

    elif num > 5000 and num <= 7500:
        real_prices.append(int(num*0.80))

    elif num > 7500:
        real_prices.append(int(num - 1500))



sum_price = sum(pricelist)
sum_price2 = sum(real_prices)

totalitems = zip(namedress, date, pricelist, real_prices)



count = 0

for file in os.listdir(r'C:\Users\Utente\Desktop\Vestiaire Folder'):
    if file.endswith('.csv'):
        count += 1


date_object = datetime.date.today()
folderv = r'C:\Users\Utente\Desktop\Vestiaire Folder'


with open(os.path.join(folderv, '{}  {} Vestiaire_doc.csv').format(count, date_object), 'a', newline='') as newfile:
    
    writer = csv.writer(newfile, dialect='excel')
    writer.writerow(['NAME OF ITEMS', 'PAYMENT', 'PRICE WITHOUT COMMISSION', 'PRICE WITH COMMISSION'])
    writer.writerow(["-----", "-----", "-----", "-----"])
    for row in totalitems:
        writer.writerow(row)

    writer.writerow(["-----------------------"])
    writer.writerow(["SUM PRICE WITHOUT COMMISSION"])
    writer.writerow([sum_price])
    writer.writerow(["SUM PRICE WITH COMMISSION"])
    writer.writerow([sum_price2])
    newfile.close()



driver.quit()
