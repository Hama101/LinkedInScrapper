from const import DRIVER , download_image , to_json , to_csv , flatten_list , login
from selenium.webdriver.common.keys import Keys
import os
import time
import random

driver = DRIVER

# a class to get data from a profile
class Condidat:
    def __init__(self, PROFILE_URL , driver , works_for):
        self.PROFILE_URL = PROFILE_URL
        self.driver = driver
        self.driver.get(PROFILE_URL)
        self.works_for = works_for
        time.sleep(3)
    
    
    def get_data(self):
        self.full_name = self.driver.find_element_by_class_name('text-heading-xlarge').get_attribute('innerHTML')
        self.img_url = self.driver.find_element_by_class_name('pv-top-card-profile-picture__image').get_attribute('src')
        download_image(f"images/{self.works_for}/",self.img_url , f"{self.full_name}.jpg")
        self.job = self.driver.find_element_by_class_name('text-body-medium').get_attribute('innerHTML')
        
        data = {
            "full_name": self.full_name,
            "img_url": self.img_url,
            "job": self.job,
        }
        #save the data to json file using json mode
        return data




#loop throw a list and iniate it condidat object than get data and append it to a new list
def get_data(profiles , works_for = None):
    data = []
    for profile in profiles:
        condidat = Condidat(PROFILE_URL=profile , driver=driver , works_for=works_for)
        try:
            c_data = condidat.get_data()
        except Exception as e:
            print("bad profile ",profile)
            continue
        print("got ----> ",c_data)
        data.append(c_data)
    return data


#the main function
def main():
    profiles = []
    time.sleep(3)
    for i in range(0,25):
        #https://www.linkedin.com/search/results/people/?keywords=tunisia&origin=CLUSTER_EXPANSION&page=3&sid=-w)
        #scrooll to the bottom of the page
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        profiles.append([x.get_attribute('href') for x in driver.find_elements_by_class_name('app-aware-link')])
        #time.sleep(2)
        driver.get(f"https://www.linkedin.com/search/results/people/?keywords=tunisia&origin=CLUSTER_EXPANSION&page={i+1}&sid=-w)")
        #time.sleep(2)
        print(f"page {i}")
    
    profiles = flatten_list(profiles)
    print("profiles ",len(profiles))
    print("profiles ",profiles[0])
    #input("press enter to continue")
    data = get_data(list(set(profiles)))
    #to_json(data)
    to_csv(data)
    # create_json(data)
    driver.close()


if __name__ == '__main__':
    login()
    main()
