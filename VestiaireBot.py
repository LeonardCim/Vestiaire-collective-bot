import configparser
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from google_trans_new import google_translator
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup as SOUP
from configparser import ConfigParser
from selenium import webdriver
import create_ini as ci
import modify_ini as mi
import run_once
import datetime
import shutil
import time
import sys
import csv
import os




print('''\nThis bot has three options:
\n- Analyze the pages of dressing with sales data
- Change the account with the data to access the page of dressing with sales
- Add a new account with which to analyze the Vestiaire pricing page.''')


def select_options_bot():
    '''Function with bot options'''

    while True:

        intro = input('''
To start the analysis enter --> "s" (only the letter) 
To change the datas of the account enter --> "m" 
To add a new account enter  --> "a"
insert: ''') 

        intro = intro.strip()
        
        if intro == 's':       #'S' stands for scrape 
            mi.check_status()
            break

        elif intro == 'c':     #'c' stands for change
            mi.select_account()
            mi.modify_ini()
            
            sys.exit()

        elif intro == 'a':      #'a' is about to add
            ci.add_user_email()
            ci.email_check()
            ci.siteURL()
            ci.site_language()
            ci.count_ini_acc()
            ci.add_acc_ini()

            sys.exit()

        elif intro != 's' or intro != 'c' or intro != 'a':
            print("\nUnrecognized command.\n's' -> analyze sales. \n'm '-> edit ini file. \n'a' -> add new account to ini file.")

select_options_bot()


from ClassLoginVestiaire import Login
password, question = Login.login_profile("\nEnter your profile password: ", "\nWrite <v> if you want to continue or <x> if you want to write the email and password again: ")


def pages_to_be_analyzed():
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

pages_to_be_analyzed()



def account_selector():
    '''Function that controls which account is active'''

    global Account

    config = ConfigParser()
    config.read(r'C:\Users\Utente\Desktop\Vestiaire Folder\vestiaire_ini.ini')
    sec_name = config.sections()

    for account in sec_name:
        if account.startswith('ACC'):
            if config[account]['Status'] == 'active':
                Account = account
            else:
                pass
    return Account

account_selector()


config = configparser()

config.read(r'C:\Users\Utente\Desktop\Vestiaire Folder\vestiaire_ini.ini')
driver_PATH = config.get(Account, 'Chromedriver-PATH')
page_url = config.get(Account, 'URL site')


try:
    driver = webdriver.Chrome(driver_PATH)
    driver.get(page_url)

except Exception as ex:
    print("Error --> {} -- URL might be wrong... Restart the program.".format(ex))
    driver.quit()
    sys.exit()
else:
    pass


try:
    cookie = WebDriverWait(driver, 15).until(
        EC.element_to_be_clickable((By.ID, 'popin_tc_privacy_button_2'))
        )
    cookie.click()

except TimeoutException:
    pass



def account_login():
    '''Small function with elements that log in to the profile.'''

    config = configparser()
    config.read(r'C:\Users\Utente\Desktop\Vestiaire Folder\vestiaire_ini.ini')
    email_profile = config.get(Account, 'User email')   

    driver.find_element_by_id('loginEmail').send_keys(email_profile), time.sleep(1)
    driver.find_element_by_id('loginPassword').send_keys(password), time.sleep(1)
    driver.find_element_by_xpath('//*[@id="popin-signup"]/div/div/div[3]/div/form/p[2]/button').click()


    orders_and_sales = WebDriverWait(driver, 15).until(
        EC.element_to_be_clickable((By.ID, 'commandes_click'))
    )
    orders_and_sales.click()

account_login()



#From this point the data collection begins

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
            pricelist.append(str(price.text.split(",")[0]))


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


def translate():
    '''Function that translates two words in the list of articles. "Return" and "sale"'''

    global tt1 #translated text
    global tt2

    config = ConfigParser()
    config.read(r'C:\Users\Utente\Desktop\Vestiaire Folder\vestiaire_ini.ini')
    lang = config.get(Account ,'Language')

    translator = google_translator()  
    translate_text1 = translator.translate('Reso', lang_tgt=lang) 
    translate_text2 = translator.translate('vendita', lang_tgt=lang)

    tt1 = translate_text1
    tt2 = translate_text2

    return tt1, tt2

translate()



initial_item = zip(namedress, date, pricelist)
not_sold = []

# removal of unsold items
for item in initial_item:

    for obj in item:
        if tt1 in obj:
            not_sold.append(item)
        elif tt2 in obj:
            not_sold.append(item)
        elif 'Item not sold or shipping.' in obj:
            not_sold.append(item)


# l --> stands for "less"
l_price = []
for money in not_sold:
    l_price.append(int(money[2]))


# the numbers go from str to int
pricelist = [int(x) for x in pricelist]


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



totalitems = zip(namedress, date, pricelist, real_prices)


sum_price = sum(pricelist)
sum_price2 = sum(real_prices)
sum_price3 = sum(l_price)


# subtraction between the sum of the prices without commission and the sum of the unsold items (without c.)
total_collection = sum_price - sum_price3


count = 0
for file in os.listdir(r'C:\Users\Utente\Desktop\Vestiaire Folder'):
    if file.endswith('.csv'):
        count += 1


# file creation date
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
    writer.writerow(['SUM TOTAL (WITH C.) MINUS UNSOLD ITEMS'])
    writer.writerow([total_collection])
    writer.writerow(['TOTAL PRICE OF ITEMS NOT SOLD'])
    writer.writerow([sum_price3])
    newfile.close()



driver.quit()

