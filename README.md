# Data-Colelction-Pipeline

# Milestone 1
Create a Github repo

# Milestone 2
This Milestone required fo rme to choose a website with an adequate amount of data that can be scraped so I have decided to collect data from MyProtein - www.myprotein.com

# Milestone 3
In the code below I used selenium to navigate through the webpages of the website until I reach and collect the weblinks of the product pages. I used 3 methods to do this:
 - Close the login pop up box upon running the website.
 -  Navigate to each section of the website
 - Scroll & click on the "view all button". This method would reveal the full product page and the URL of the page would be added to the list.
 This procedure was repeated 5 times, for the 5 different product pages on that website.


from inspect import Attribute
from time import sleep
from tkinter import E
from selenium import webdriver
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.common.by import By

class Scraper():
    def __init__(self,URL):
        self.driver = webdriver.Edge(EdgeChromiumDriverManager().install())
        self.URL = ("https://www.myprotein.com/")
        self.DropDown_XPaths = [['//a[@href="/nutrition.list"]', '//a[@href="/nutrition/bestsellers-en-gb.list"]'],
                    ['//a[@href="/clothing.list"]', '//a[@href="/clothing/outlet.list"]'],
                    ['//a[@href="/nutrition/healthy-food-drinks.list"]'],
                    ['//a[@href="/nutrition/vitamins.list"]', '//a[@href="/nutrition/vitamins-minerals.list"]'],
                    ['//a[@href="/nutrition/vegan.list"]' , '//a[@href="/dietary-needs/vegan.list"]']]
        print(self.DropDown_XPaths[0][1])
        self.Webpage_links_list = []
    
    def login_bypass(self):
        self.driver.find_element( By.CLASS_NAME, 'emailReengagement_close_button').click()
    
    def Navigate(self,DropDown_XPaths):
        click_Drop_down = self.driver.find_element(By.XPATH, DropDown_XPaths[0])
        sleep(2)
        Drop_Down_link = click_Drop_down.get_attribute("href")
        sleep(2)
        print(Drop_Down_link )
        self.driver.get(Drop_Down_link )
        
    def Scroll(self,DropDown_XPaths):
        try:
            View_All = self.driver.find_element(By.XPATH, '//div[@class="sectionPeek componentWidget"]')
            self.driver.execute_script("arguments[0].scrollIntoView();",View_All)
            sleep(2)
            view_all_redirect = self.driver.find_element(By.XPATH, DropDown_XPaths[1]).get_attribute("href")
            self.driver.get(view_all_redirect)
        except Exception as e:
            print(e)
        self.Webpage_links_list.append(self.driver.current_url)
        sleep(3)
    
    def Webpage_links(self):
        for i in range (0,4):
            self.Navigate(self.DropDown_XPaths[i])
            self.Scroll(self.DropDown_XPaths[i])
        print (self.Webpage_links_list)

def Website(URL):
    MyProtein = Scraper(URL)
    MyProtein.driver.get(MyProtein.URL)
    sleep(3)
    MyProtein.login_bypass()
    MyProtein.Webpage_links()
    
    
    
if __name__ == "__main__":
    URL= ("https://www.myprotein.com/")
    Website(URL)


# Milestone 4 - scraping images and Information
In this Milestone I was tasked to scrape all the important information from the links that I collected in the previous Milestone. In order to do this I knew I first had to create two methods; the first scraping all the product images from the page and the second scraping all the relevant information (product-id, name , price).
I then created a dictionary for the product information so that each product would be assigned to a UUID as the key and the values would be the relevant information scraped in a list format.

    def product_image(self):
        image_src = []
        image = self.driver.find_elements(By.XPATH, '//*[@data-track="product-image"]')    
        for element in image:
            image_src.append(element.get_attribute("src"))
        return image_src
        


    def product_info(self):
        product_id = self.driver.find_elements(By.XPATH, '//*[@class="js-enhanced-ecommerce-data athenaProductBlock_hiddenElement"]')
        Data_dict = {}
        for element in product_id:
            Data_dict.setdefault(str(uuid.uuid4()),[element.get_attribute("data-product-id"),element.get_attribute("data-product-title"),element.get_attribute("data-product-price")])
        return Data_dict

After creating the 'Data.dict' variable, I needed to append image src inforamation to the newly created dictionary. This meant that I needed to create another method where the values in dictionary would append iteratively. 
    def scrape(self):
        idx=0
        fill_image_src=self.product_image()
        attribute_dict = self.product_info()
        for key,value in attribute_dict.items():
            value.append(fill_image_src[idx])
            attribute_dict[key] = value
            idx +=1
        return attribute_dict

I then had to ensure that this program would run iteratively for each product page, where each product page would have their own dictionary. 
def Website(URL):
    MyProtein = Scraper(URL)
    MyProtein.driver.get(MyProtein.URL)
    sleep(3)
    MyProtein.login_bypass()
    MyProtein.webpage_links()
    for i in MyProtein.webpage_link_list:
        MyProtein.driver.get(i)
        page_dict = MyProtein.scrape()
        MyProtein.data_list.append(page_dict)
    print(MyProtein.data_list)

The final part of this Milestone was to create a folder and store all data that was scraped in a json file. I also needed to download all the images from the src links and store them in a folder called "images".

Below are the methods I created to accomplish this part of the Milestone, along with the final version of the code:

Make relevant directories:
def make_dir():
    folders = ["raw_data","images"]
    for dir in range (len(folders)):
        directory = folders[dir]
        parent_direct = 'C:\\Users\\nadir\\Data_Collection_Pipeline'
        path = os.path.join(parent_direct,directory)
        try:
            os.mkdir(path)
        except OSError as error:
            print(error)

Create Json file:
    def json_file_save(self):
        with open("data.json", "w") as f:
            json.dump(self.data_list,f)
        json_file = "data.json"
        destination = "C:\\Users\\nadir\\Data_Collection_Pipeline\\raw_data\\data.json"
        try:
            os.replace(json_file,destination)
        except FileNotFoundError:
            print(json_file+"was not found")


Image Downloader method:
    def image_downloader(self):
        info = self.scrape()
        for value in info.items():
            product_id = value[0]
            product_name = value[1]
            image = value[3]
    
            with open(product_name.replace(" ", "_").replace(":","-")[:12] +"-" + product_id + ".jpg", "wb") as f:
                im = requests.get(image)
                f.write(im.content)
            image_file = "{0}-{1}.jpg".format(product_name.replace(" ", "_").replace(":","-")[:12], product_id)
            destination = "C:\\Users\\nadir\\Data_Collection_Pipeline\\images\\{0}".format(image_file)
            try:
                os.replace(image_file,destination)
            except FileNotFoundError:
                print(image_file+"was not found")

Program functionality method:
def Website(URL):
    MyProtein = Scraper(URL)
    MyProtein.driver.get(MyProtein.URL)
    sleep(3)
    MyProtein.login_bypass()
    MyProtein.webpage_links()
    for i in MyProtein.webpage_link_list:
        MyProtein.driver.get(i)
        MyProtein.image_downloader()
        page_dict = MyProtein.scrape()
        MyProtein.data_list.append(page_dict)
    print(MyProtein.data_list)
    MyProtein.json_file_save()

Final code:
import requests
import json
import os
import uuid
from time import sleep
from selenium import webdriver
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.common.by import By

class Scraper():
    def __init__(self,URL):
        self.driver = webdriver.Edge(EdgeChromiumDriverManager().install())
        self.URL = ("https://www.myprotein.com/")
        self.dropdown_xpaths = [['//a[@href="/nutrition.list"]', '//a[@href="/nutrition/bestsellers-en-gb.list"]'],
                    ['//a[@href="/clothing.list"]', '//a[@href="/clothing/outlet.list"]'],
                    ['//a[@href="/nutrition/healthy-food-drinks.list"]'],
                    ['//a[@href="/nutrition/vitamins.list"]', '//a[@href="/nutrition/vitamins-minerals.list"]'],
                    ['//a[@href="/nutrition/vegan.list"]' , '//a[@href="/dietary-needs/vegan.list"]']]
        self.webpage_link_list = []
        self.data_list = []
        
    
    def login_bypass(self):
        self.driver.find_element( By.CLASS_NAME, 'emailReengagement_close_button').click()
    
    def navigate(self,dropdown_xpaths):
        click_drop_down = self.driver.find_element(By.XPATH, dropdown_xpaths[0])
        sleep(2)
        drop_down_link = click_drop_down.get_attribute("href")
        sleep(2)
        self.driver.get(drop_down_link )
        
    def scroll(self,dropdown_xpaths):
        try:
            view_All = self.driver.find_element(By.XPATH, '//div[@class="sectionPeek componentWidget"]')
            self.driver.execute_script("arguments[0].scrollIntoView();",view_All)
            sleep(2)
            view_all_redirect = self.driver.find_element(By.XPATH, dropdown_xpaths[1]).get_attribute("href")
            self.driver.get(view_all_redirect)
        except Exception as e:
            print(e)
        self.webpage_link_list.append(self.driver.current_url)
        sleep(3)
    
    def webpage_links(self):
        for i in range (0,4):
            self.navigate(self.dropdown_xpaths[i])
            self.scroll(self.dropdown_xpaths[i])
    
    def product_image(self):
        image_src = []
        image = self.driver.find_elements(By.XPATH, '//*[@data-track="product-image"]')    
        for element in image:
            image_src.append(element.get_attribute("src"))
        return image_src
        


    def product_info(self):
        product_id = self.driver.find_elements(By.XPATH, '//*[@class="js-enhanced-ecommerce-data athenaProductBlock_hiddenElement"]')
        Data_dict = {}
        for element in product_id:
            Data_dict.setdefault(str(uuid.uuid4()),[element.get_attribute("data-product-id"),element.get_attribute("data-product-title"),element.get_attribute("data-product-price")])
        return Data_dict
            
    def scrape(self):
        idx=0
        fill_image_src=self.product_image()
        attribute_dict = self.product_info()
        for key,value in attribute_dict.items():
            value.append(fill_image_src[idx])
            attribute_dict[key] = value
            idx +=1
        return attribute_dict
    
    def json_file_save(self):
        with open("data.json", "w") as f:
            json.dump(self.data_list,f)
        json_file = "data.json"
        destination = "C:\\Users\\nadir\\Data_Collection_Pipeline\\raw_data\\data.json"
        try:
            os.replace(json_file,destination)
        except FileNotFoundError:
            print(json_file+"was not found")
        
            
    def image_downloader(self):
        info = self.scrape()
        for value in info.items():
            product_id = value[0]
            product_name = value[1]
            image = value[3]
    
            with open(product_name.replace(" ", "_").replace(":","-")[:12] +"-" + product_id + ".jpg", "wb") as f:
                im = requests.get(image)
                f.write(im.content)
            image_file = "{0}-{1}.jpg".format(product_name.replace(" ", "_").replace(":","-")[:12], product_id)
            destination = "C:\\Users\\nadir\\Data_Collection_Pipeline\\images\\{0}".format(image_file)
            try:
                os.replace(image_file,destination)
            except FileNotFoundError:
                print(image_file+"was not found")
def Website(URL):
    MyProtein = Scraper(URL)
    MyProtein.driver.get(MyProtein.URL)
    sleep(3)
    MyProtein.login_bypass()
    MyProtein.webpage_links()
    for i in MyProtein.webpage_link_list:
        MyProtein.driver.get(i)
        MyProtein.image_downloader()
        page_dict = MyProtein.scrape()
        MyProtein.data_list.append(page_dict)
    print(MyProtein.data_list)
    MyProtein.json_file_save()

    
def make_dir():
    folders = ["raw_data","images"]
    for dir in range (len(folders)):
        directory = folders[dir]
        parent_direct = 'C:\\Users\\nadir\\Data_Collection_Pipeline'
        path = os.path.join(parent_direct,directory)
        try:
            os.mkdir(path)
        except OSError as error:
            print(error)
if __name__ == "__main__":
    URL= ("https://www.myprotein.com/")
    make_dir()
    Website(URL)

