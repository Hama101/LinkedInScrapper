from selenium import webdriver
import time
import os
import requests
import io
from PIL import Image
import json
import pandas as pd

from secrects import EMAIL , PASSWORD

PATH = r'driver\chromedriver.exe'
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--incognito")
# chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--disable-java")

driver = webdriver.Chrome(PATH , chrome_options=chrome_options)

# url = driver.command_executor._url
# session_id = driver.session_id
# driver = webdriver.Remote(command_executor=url,desired_capabilities={})

# driver.session_id = session_id
# driver.get("http://www.mrsmart.in")

DRIVER = driver

def download_image(download_path, url, file_name):
	#delete "\n" from the folder name
	download_path = download_path.replace("\n", "")
	#creating folder if not exists    
	if not os.path.isdir(download_path):
		os.makedirs(download_path)
		print("Created folder: " + download_path)

	try:
		image_content = requests.get(url).content
		image_file = io.BytesIO(image_content)
		image = Image.open(image_file)
		file_path = download_path + file_name

		with open(file_path, "wb") as f:
			image.save(f, "JPEG")

		print("Success")
		return True
	except Exception as e:
		print('FAILED -', e)
		return False



def to_csv(data):
	df = pd.DataFrame(data)
	df.to_csv('data.csv', index=False)


def to_json(data):
	#use pandas to convert list to dataframe
	df = pd.DataFrame(data)
	#convert dataframe to json
	json_data = df.to_json('data.json')



def flatten_list(t):
    flat_list = []
    for sublist in t:
        try :
            for item in sublist:
                flat_list.append(item)
        except :
            flat_list.append(sublist)
    return flat_list



# a log in function
def login():
	driver.get("https://www.linkedin.com/login?fromSignIn=true&trk=guest_homepage-basic_nav-header-signin")
	time.sleep(3)
	driver.find_element_by_id('username').send_keys(EMAIL)
	driver.find_element_by_id('password').send_keys(PASSWORD)
	driver.find_element_by_xpath('//*[@id="organic-div"]/form/div[3]/button').click()
	time.sleep(3)
    #switch to the login window
    #test@2020
    #leyapeb522@kruay.com