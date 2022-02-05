from const import DRIVER , download_image , to_json , to_csv , flatten_list , login
from selenium.webdriver.common.keys import Keys
import os
import time
import random

driver = DRIVER


class StartUp:
    def __init__(self, PROFILE_URL , driver):
        self.PROFILE_URL = PROFILE_URL
        self.driver = driver
        self.driver.get(PROFILE_URL)
        time.sleep(3)
    
    
    def get_data(self):
        self.full_name = self.driver.find_element_by_class_name('t-24').find_element_by_tag_name('span').get_attribute('innerHTML')
        self.username = f"{self.full_name.replace(' ','')}{random.randint(1,1000)}"
        self.email = f"{self.username}@gmail.com"
        self.img_url = self.driver.find_element_by_class_name('org-top-card-primary-content__logo').get_attribute('src')
        download_image("images/",self.img_url , f"{self.username}.jpg")
        self.bio = self.driver.find_element_by_class_name('org-top-card-summary__tagline').get_attribute('innerHTML')
        
        data = {
            "full_name": self.full_name,
            "username": self.username,
            "email": self.email,
            "img_url": self.img_url,
            "bio": self.bio,
        }
        return data


#loop throw a list and iniate it condidat object than get data and append it to a new list
def get_data(profiles):
    data = []
    for profile in profiles:
        start_up = StartUp(PROFILE_URL=profile , driver=driver)
        try:
            c_data = start_up.get_data()
        except Exception as e:
            print("bad profile ",profile)
            continue
        print("got ----> ",c_data)
        data.append(c_data)
    return data




def main():
    profiles = []
    time.sleep(3)
    for i in range(0,10):
        #https://www.linkedin.com/search/results/people/?keywords=tunisia&origin=CLUSTER_EXPANSION&page=3&sid=-w)
        #scrooll to the bottom of the page
        driver.get(f"https://www.linkedin.com/search/results/companies/?keywords=tunisia&origin=GLOBAL_SEARCH_HEADER&page={i}&sid=WF!")
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        l = [x.get_attribute('href') for x in driver.find_elements_by_class_name('app-aware-link')]
        profiles.append(l)
        #profiles = [profile for profile in profiles if 'company' in profile]
        #time.sleep(2)
        #time.sleep(2)
        print(f"page {i}")
    
    profiles = flatten_list(profiles)
    print("profiles ",len(profiles))
    print("profiles ",profiles)
    #input("press enter to continue")
    data = get_data(list(set(profiles)))
    #to_json(data)
    to_csv(data)
    # create_json(data)
    driver.close()


if __name__ == "__main__":
    login()
    main()