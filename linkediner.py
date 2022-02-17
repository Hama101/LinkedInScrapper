from const import DRIVER , download_image , to_json , to_csv , flatten_list , login
from selenium.webdriver.common.keys import Keys
import json
import solver as s
import random
import time , os
driver = DRIVER


def new_tab(url):
    driver.execute_script(f"window.open('{url}');")


def change_foucs(index):
    driver.switch_to.window(driver.window_handles[index])


#this founction is used to set the phone numbers in a json file
def set_phones():
    driver.get("https://receive-smss.com/")
    time.sleep(5)
    #scroll down
    #driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    holders = driver.find_elements_by_class_name('number-boxes-item')
    numbers = []
    for holder in holders:
        try:
            number = {
                "phone" : holder.find_element_by_tag_name("h4").get_attribute("innerHTML"),
                "country" : holder.find_element_by_tag_name("h5").get_attribute("innerHTML"),
                "type": holder.find_elements_by_class_name("number-boxes-item-button")[0].get_attribute("innerHTML"), 
                "url": holder.find_elements_by_tag_name("a")[1].get_attribute("href"),
            }
            print(number)
            numbers.append(number)
        except Exception as e:
            print(e)
            continue
    #save numbers to phones.json
    with open('phones.json','w') as f:
        json.dump(numbers,f,indent=4)


#select a random open phone number from phones.json
def get_phone():
    with open('phones.json','r') as f:
        phones = json.load(f)
    #filter phones numbers to get the numbers with type = Open
    open_phones = [phone for phone in phones if phone['type'] == 'Open']
    random_phone = random.choice(open_phones)
    return random_phone



def solve_capchat(page):
    #driver.find_element_by_xpath(f'//*[@id="register-form-captcha-recaptcha-{page}-form"]').click()
    s.main(driver)
    
    if page == 'login':
        driver.find_element_by_xpath('//*[@id="login-form"]/button').click()
    elif page == 'registration':
        driver.find_element_by_xpath('//*[@id="registration-form"]/button').click()


def genrate_a_string(type = False):
    #define a list of all charaters
    alphabet = ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]
    upper_alphabets = [a.upper() for a in alphabet]
    if type:
        num_charaters = [a for a in range(0,10)]
        symbols = ["@","!","?"]
    else:
        num_charaters = []
        symbols = []
    #combine all the charaters
    all_charaters = alphabet + upper_alphabets + num_charaters + symbols
    #shuffle the list
    random.shuffle(all_charaters)
    #get random 10 charaters
    random_charaters = random.sample(all_charaters,random.randint(8,13))
    #join the charaters
    random_string = ""
    for charater in random_charaters:
        random_string += str(charater)

    return random_string


def set_temp_mail():
    time.sleep(8)
    email = driver.find_element_by_id('mail').get_attribute('value')
    print(email)
    input("press enter to continue...")
    return email


def inser_phone(data , phone):
    time.sleep(2)
    country = phone['country']
    input("press enter to continue...")
    selector = driver.find_element_by_id('select-register-phone-country')
    selector.click()
    options = selector.find_elements_by_tag_name('option')
    options_text = [option.get_attribute("innerHTML").upper() for option in options]
    print(options_text)
    input("press enter to continue...")
    #get the index of cuntrey in the options_text
    index = options_text.index(country)
    print(index)
    #select the country
    options[index].click()
    extension = str(options[index].get_attribute("extension"))
    extension = extension.replace(" ","")
    time.sleep(1)
    print(extension)
    f_phone = data["phone"].replace(extension,"")
    print(f_phone)

    input("press enter to continue...")
    driver.find_element_by_id('register-verification-phone-number').send_keys(f_phone)
    btn = driver.find_element_by_id('register-phone-submit-button')
    btn.click()
    time.sleep(2)


def register(phone):
    driver.get(phone['url'])
    country = phone['country'].upper()
    time.sleep(2)
    page = 'registration'

    new_tab('https://temp-mail.org/en/')
    time.sleep(2)
    change_foucs(1)

    data = {
        "phone" : phone['phone'],
        "email" : set_temp_mail(),
        "name" : genrate_a_string(),
        "last_name" : genrate_a_string(),
        "password" : genrate_a_string(type = True),
    }

    print("data ",data)
    input("press enter to continue...")
    new_tab("https://www.linkedin.com/signup/")
    change_foucs(2)
    time.sleep(5)
    driver.find_element_by_id('email-address').send_keys(data['email'])
    time.sleep(1)
    driver.find_element_by_id('password').send_keys(data["password"])
    time.sleep(1)
    btn = driver.find_element_by_id('join-form-submit')
    btn.click()
    time.sleep(1)
    driver.find_element_by_id('first-name').send_keys(data["name"])
    time.sleep(1)
    driver.find_element_by_id('last-name').send_keys(data["last_name"])
    time.sleep(1)
    btn = driver.find_element_by_id('join-form-submit')
    btn.click()

    time.sleep(5)
    input("press enter to continue...")
    try:
        solve_capchat(page)
    except Exception as e:
        input("Please solbve the captcha than press enter!!!!")
    #switch to frame
    frames = driver.find_elements_by_tag_name("iframe")
    print([frame.get_attribute("title") for frame in frames])
    for frame in frames:
        if "Security verification" == frame.get_attribute("title"):
            print("Security verification")
            driver.switch_to.frame(frame)
            time.sleep(6)
            inser_phone(data , phone)
            break


    #save phone and password to keys.txt
    with open('keys.txt','a') as f:
        f.write(f'{data["phone"]};{data["password"]}\n')




if __name__ == "__main__":
    phone = get_phone()
    print("phone:",phone)
    register(phone)
    driver.quit()