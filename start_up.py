from const import DRIVER , download_image , to_json , to_csv , flatten_list , login
from selenium.webdriver.common.keys import Keys
import json
import os
import time
import random
from condidat import Condidat , get_data

driver = DRIVER


class StartUp:
    def __init__(self, PROFILE_URL , driver):
        self.PROFILE_URL = PROFILE_URL
        self.driver = driver
        self.driver.get(PROFILE_URL)
        time.sleep(3)
    
    def get_employess(self):
        url = self.driver.find_element_by_class_name('mt1').find_element_by_tag_name('a').get_attribute('href')
        self.driver.get(url)
        time.sleep(2)
        n_url = self.driver.current_url
        employees = []
        for i in range(0,1):
            try:        
                #click on the button and save the url
                time.sleep(2)
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(2)
                l = [x.get_attribute('href') for x in driver.find_elements_by_class_name('app-aware-link')]
                employees.append(l)
                driver.get(f"{n_url}&page={i+1}")
            except Exception as e:
                print(e)
                break

        #romve the duplicates from the list
        employees = list(set(flatten_list(employees)))
        #getting the data from the profiles
        data = get_data(profiles=employees , works_for=self.full_name)
        return data
    
    def get_data(self):
        self.full_name = self.driver.find_element_by_class_name('t-24').find_element_by_tag_name('span').get_attribute('innerHTML')
        self.img_url = self.driver.find_element_by_class_name('org-top-card-primary-content__logo').get_attribute('src')
        download_image("images/startups/",self.img_url , f"{self.full_name}.jpg")
        self.bio = self.driver.find_element_by_class_name('org-top-card-summary__tagline').get_attribute('innerHTML')
        
        #get the code sr of the page than save it to html file
        code_sr = self.driver.page_source
        with open(f"html_files/startups/{self.full_name}.html" , 'w' , encoding='utf-8') as f:
            f.write(code_sr)
        
        data = {
            "full_name": self.full_name,
            "img_url": self.img_url,
            "bio": self.bio,
            "employees": self.get_employess()
        }
        #save the data to json file using json model
        with open(f"json_files/startups/{self.full_name}.json" , 'w' , encoding='utf-8') as f:
            json.dump(data , f , indent=4)
        
        return data


def take_a_break():
    print("taking a break")
    time.sleep(random.randint(5,10))
    driver.get("https://www.linkedin.com/feed/")
    #scroll throw the feed slowly
    for i in range(0,10):
        time.sleep(1)
        driver.execute_script(f"window.scrollTo(0, {i*1000});")
        likes_btn = driver.find_elements_by_class_name('reactions-react-button')
        #get a sample from the likes_btn
        if likes_btn:
            likes_btn[random.randint(0,len(likes_btn)-1)].click()
            time.sleep(1)
            likes_btn[random.randint(0,len(likes_btn)-1)].click()
            time.sleep(2)
            likes_btn[random.randint(0,len(likes_btn)-1)].click()
            time.sleep(2)
            likes_btn[random.randint(0,len(likes_btn)-1)].click()
            time.sleep(2)
        else:
            continue
        time.sleep(1)



#loop throw a list and iniate it condidat object than get data and append it to a new list
def s_get_data(profiles):
    data = []
    for index , profile in enumerate(profiles):
        start_up = StartUp(PROFILE_URL=profile , driver=driver)
        try:
            c_data = start_up.get_data()
        except Exception as e:
            print("bad profile ",profile)
            continue
        print("got ----> ",c_data)
        data.append(c_data)
        if index == 10:
            take_a_break()
    return data




def main():
    profiles = []
    with open('startups.txt' , 'r') as f:
        for line in f:
            profiles.append(line.strip())
    print("profiles---> ",profiles)
    #input("press enter to continue")
    data = s_get_data(list(set(profiles)))
    driver.close()


if __name__ == "__main__":
    login()
    main()