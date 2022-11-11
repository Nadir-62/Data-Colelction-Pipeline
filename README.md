# Data-Collection-Pipeline

# Milestone 1
Create a Github repo

# Milestone 2
This Milestone required for me to choose a website with an adequate amount of data that can be scraped so I have decided to collect data from MyProtein - www.myprotein.com

# Milestone 3
In the code below I used selenium to navigate through the webpages of the website until I reach and collect the weblinks of the product pages. I used 3 methods to do this:
 - Close the login pop up box upon running the website.
 -  Navigate to each section of the website
 - Scroll & click on the "view all button". This method would reveal the full product page and the URL of the page would be added to the list.
 This procedure was repeated 5 times, for the 5 different product pages on that website.

'''
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
'''

# Milestone 4 - scraping images and Information
In this Milestone I was tasked to scrape all the important information from the links that I collected in the previous Milestone. In order to do this I knew I first had to create two methods; the first scraping all the product images from the page and the second scraping all the relevant information (product-id, name , price).
I then created a dictionary for the product information so that each product would be assigned to a UUID as the key and the values would be the relevant information scraped in a list format.
'''
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
'''
I then had to ensure that this program would run iteratively for each product page, where each product page would have their own dictionary. 
'''
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
'''
The final part of this Milestone was to create a folder and store all data that was scraped in a json file. I also needed to download all the images from the src links and store them in a folder called "images".

Below are the methods I created to accomplish this part of the Milestone, along with the final version of the code:

Make relevant directories:
'''
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
'''
Create Json file:
'''
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
'''
Program functionality method:
'''
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
'''
Final code:
'''
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
''' 
 ## Milestone 5 Documentation and Testing
 In this Milestone I took steps to optimise and improve the code written above. The first aspect of the code that I tested was to check the duration of the scraper.
 I did this by creating a "timer decorator" as shown below:
 '''
 def timer(func):
    def wrapper(*args, **kwargs):
        t1 = time()
        result = func(*args,**kwargs)
        t2 = time()
        print(f"time taken = {t2-t1} ms")
        return result
    return wrapper
'''
This decorator was used to check the duratation of the code aswell as individual functions which made it easier to idedntify which areas of the code
were inefficient. 

After implementing this timer I was able to improve the time efficiency of my code by 30 seconds by altering the code into the program below:
'''
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from time import sleep,time
from webdriver_manager.chrome import ChromeDriverManager

import boto3
import csv
import json
import os
import pandas as pd
import requests
import uuid

class Scraper():
    """ 
    This class is used to scrape data from a website.
    
    Attributes:
    driver: webdriver 
    URL(str) : The source of the scraped data
    webpage_link_list(list): List of product page URLs
    data_list (list): list of dictionaries which contain all the scraped information for each product page
    page_titles (list): list of product pages
    page_idx(int) : This is used to iterate when creating the folders for the image sub-folders.
    
    """
    def __init__(self,URL):
        chrome_options = self.generate_options()
        self.driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)
        self.URL = ("https://www.myprotein.com/")
        self.homepage_links =[]
        self.data_list = []
        self.page_titles =[] 
        self.page_idx=0
        
    def timer1(func):
        def wrapper(*args, **kwargs):
            t1 = time()
            result = func(*args,**kwargs)
            t2 = time()
            print(f"time taken = {t2-t1} ms")
            return result
        return wrapper    
 
    def navigate(self):
        """This function navigates through the homepage to each individual section. It also collects the titles of each section"""
        click_drop_down = self.driver.find_elements(By.XPATH, '//a[@class="responsiveFlyoutMenu_levelOneLink responsiveFlyoutMenu_levelOneLink-hasChildren"]')
        for links in click_drop_down[0:5]:
            title = links.get_attribute("data-context")
            drop_down_link = links.get_attribute("href")
            self.homepage_links.append(drop_down_link)
            self.page_titles.append(title)
        self.image_folder()
        
    def scroll(self):
        """This function locates the product pages and then collects the URL of each page."""
        try:
            try:
                view_all_redirect = self.driver.find_element(By.XPATH, '//*[@class="sectionPeek_allCta"]').get_attribute("href")
                self.driver.get(view_all_redirect)
            except Exception:
                view_all_redirect2 = self.driver.find_element(By.XPATH,'//*[@class="sectionPeek_allCta sectionPeek_allCta-show"]').get_attribute("href")
                self.driver.get(view_all_redirect2)
        except Exception as e: 
            print(e)
        sleep(1)
        
    def product_page_scraper(self):
        """This navigates the website 5 times for each section, collecting their product page URL and then creating an image folder."""
        self.driver.find_element( By.CLASS_NAME, 'emailReengagement_close_button').click()
        self.navigate()
        for link in range (len(self.homepage_links)):
            self.driver.get(self.homepage_links[link])
            self.scroll()
            self.image_downloader()
            page_dict = self.scrape()
            self.data_list.append(page_dict)
            self.page_idx +=1
        print(self.page_titles)
    
    def product_image(self):
        """This collects all the src tags for all the images on the product page.All of this information is then added to a list"""
        image_src = []
        image = self.driver.find_elements(By.XPATH, '//*[@data-track="product-image"]')    
        for element in image:
            image_src.append(element.get_attribute("src"))
        return image_src
        


    def product_info(self):
        """This collects all the relevent information for every product on the produuct page. This includes the ProductID, Name and price. 
        All of this information is then added to a dictionary. Each item in the dictionary has a UUID as the key"""
        product_id = self.driver.find_elements(By.XPATH, '//*[@class="js-enhanced-ecommerce-data athenaProductBlock_hiddenElement"]')
        Data_dict = {}
        for element in product_id:
            Data_dict.setdefault(str(uuid.uuid4()),[element.get_attribute("data-product-id"),element.get_attribute("data-product-title"),element.get_attribute("data-product-price")])
        return Data_dict
    
    
    def scrape(self):
        """This function appends the dictionary created in the product_info method with the 
        list of src tags created in the product_image method"""
        idx=0
        fill_image_src=self.product_image()
        attribute_dict = self.product_info()
        for key,value in attribute_dict.items():
            value.append(fill_image_src[idx])
            attribute_dict[key] = value
            idx +=1
        return attribute_dict
    
    def json_file_save(self):
        """This method creates a json file for the data that collected across the 5 product pages. It is located in the folder raw_data"""
        with open("data.json", "w") as f:
            json.dump(self.data_list,f)
        json_file = "data.json"
        destination = "/raw_data/data.json"
        
        try:
            os.replace(json_file,destination)
        except FileNotFoundError:
            print(json_file+"was not found")
        
        
        
        

    def s3_bucket(self,destination):
        bucket = "nadirsmyprotiendata"
        self.json_file_save()
        self.s3.upload_file(destination, bucket, "MyProtein_data.json")

        
    def image_downloader(self):
        """
        This function extracts the src links from the dictionary and downloads the images.
        After the images are downloaded the images are then moved to the appropriate folder
        which corresponds to their category.
        """
        info = self.scrape()
        for key,value in info.items():
            product_id = value[0]
            product_name = value[1]
            image = value[3]
        #     bucket_names = str("nadirsmyprotien" + str(self.page_titles[self.page_idx].lower().replace(",","-").replace("&", "and").replace(" ","-")))
        #     try:
        #         try:
        #             bucket = self.s3.create_bucket(Bucket=bucket_names,CreateBucketConfiguration={
        # 'LocationConstraint': 'eu-west-2',})
        #         except:
        #             bucket = bucket_names
        #     except Exception as e:
        #         print(e)
    
            with open(product_name.replace(" ", "_").replace(":","-")[:12] +"-" + product_id + ".jpg", "wb") as f:
                # Here the file name is created according to the product name and ID. 
                im = requests.get(image)
                f.write(im.content)
            image_file = str("{0}-{1}.jpg".format(product_name.replace(" ", "_").replace(":","-")[:12], product_id))
            destination = str("/images/{0}/{1}".format(self.page_titles[self.page_idx],image_file))
            try:
                os.replace(image_file,destination)
                #self.s3.upload_file(destination, str(bucket), image_file)

            except FileNotFoundError:
                print(image_file+" was not found")
            

    def image_folder(self):
        """ 
        This function creates the image folders for each product page. 
        The list of page titles that was appended in the navigate function are used to do this.
        All of these pages are located within the parent folder images
        """
        for page in range (len(self.page_titles)):
            directory = self.page_titles[page]
            parent_direct = '/images'
            path = os.path.join(parent_direct,directory)
            try:
                os.mkdir(path)
            except OSError as error:
                print(error)
                
    def format_data(self):
        file= open ("/raw_data/data.json")
        raw_data = json.load(file)
        df = pd.DataFrame.from_dict(raw_data[0], orient ="index" ,columns = ["Product ID" , "Product Name", "Price", "Image Link"]) 
        df.to_csv( "/raw_data/formatted_data.csv", mode= "w" , header = True, index=True )
        
        for i in range (1, len(raw_data)):
            df = pd.DataFrame.from_dict(raw_data[i], orient= "index", columns = ["Product ID" , "Product Name", "Price", "Image Link"]) 
            df.to_csv( "/raw_data/formatted_data.csv", mode= "a" , header = False, index=True )
            print(df)
            i +=1
            
        file2 = pd.read_csv( "/raw_data/formatted_data.csv")
        duplicates = file2[file2.duplicated(subset=["Product ID"])]
        print(duplicates)
        file2.drop_duplicates(subset = ["Product ID"], keep = "first")
        file2.to_csv( "/raw_data/formatted_data.csv", index=True)

def timer(func):
    def wrapper(*args, **kwargs):
        t1 = time()
        result = func(*args,**kwargs)
        t2 = time()
        print(f"time taken = {t2-t1} ms")
        return result
    return wrapper   
@timer             
def Website(URL):
    """ 
    This is the overall functionality of the program.
    - Firstly the Website URL is obtained
    - Next the homepage is navigated until the url of all the product pages is collected.
    - After that all the images from that page are downloaded and stored in their appropriate folders
    - Then all the relevant information is scraped from that product page and stored in a dictionary.
    - And then this is added to a data list after which the process is repeated for the other 4 product 
      pages.   
    - Finally the data dictionary is printed and the saved as a json file.
    """
    MyProtein = Scraper(URL)
    MyProtein.driver.get(MyProtein.URL)
    sleep(2)
    MyProtein.product_page_scraper()
    print(MyProtein.data_list)
    MyProtein.json_file_save()
    MyProtein.format_data()
    MyProtein.driver.quit()
    
def make_dir():
    """ 
    This function creates 2 folders. 1 for the raw data and the other for the images.    
    """
    folders = ["raw_data","images"]
    for dir in range (len(folders)):
        directory = folders[dir]
        parent_direct = '/'
        path = os.path.join(parent_direct,directory)
        try:
            os.mkdir(path)
        except OSError as error:
            print(error)

                            
if __name__ == "__main__":
    URL= ("https://www.myprotein.com/")
    make_dir()
    Website(URL)
'''

## MileStone 6 - Containerising the scraper

In this Milestone I learnt how to use Docker Containers and Images. This was done so that this program can be run on any machine. However as Docker does not use
a GUI I had to ensure that the scraper was in headless mode. This was done using the Function below:

'''
    def generate_options(self):
        chrome_options = Options()
        chrome_options.add_argument("--disable-notifications")
        chrome_options.add_argument('no-sandbox') 
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("disable-dev-shm-usage")
        return chrome_options
'''
After that I used created a Docker file to build my Docker Image as shown below:
'''
FROM python:3.10.4

RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - &&\
    sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list' &&\
    apt-get -y update &&\
    apt-get install -y google-chrome-stable &&\
    wget -O /tmp/chromedriver.zip http://chromedriver.storage.googleapis.com/`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE`/chromedriver_linux64.zip &&\
    apt-get install -yqq unzip &&\
    unzip /tmp/chromedriver.zip chromedriver -d /usr/local/bin/ 

COPY . .
RUN pip install -r requirements.txt
ENTRYPOINT ["python", "Data_scraper.py"]
'''
This Docker Image was able to run this program on a Linux Operating system.

Finally after building the docker image on my local account I had to push the image onto docker hub by first creating a docker repository renaming the docker to match my repository and then using:

docker push nadir62/data_scraper_docker2

## MileStone 7 - Set up a CI/CD pipline for my Docker image

In this Milestone I created a CI Pipline on Github that would push my Docker Container on to the Docker hub

The first thing that was required of me was to add "secret variables" to my Github. These variables include the Docker ID and the Personal Access Token (Password equivalent)
of my Dockerhub. 

After doing this I created an workflow and ran the YML file as seen below:
'''
name: ci

on:
  push:
    branches:
      - "main"
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v3
      - name: Login to Docker Hub
        uses: docker/login-action@v2
        with:
          username: ${{ secrets.DOCKER_HUB_USERNAME }}
          password: ${{ secrets.DOCKER_HUB_ACCESS_TOKEN }}
      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v2
      - name: Build and push
        uses: docker/build-push-action@v3
        with:
          context: .
          file: ./Dockerfile
          push: true
          tags: ${{ secrets.DOCKER_HUB_USERNAME }}/clockbox:latest
'''

This YML file would automate the build of my Image and then upload it to the Dockerhub, using the "secret" variables that I applied in the previous step.

As you can see in the image below after a few minutes the docker image was uploaded to the Dockerhub.

![image](https://user-images.githubusercontent.com/112514576/200587975-e7a88dfa-1049-4cae-9aec-21a0f6158cc4.png)


